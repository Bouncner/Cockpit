"""Functions defining workers.

Workers run in pools and are started by other components.
"""
from multiprocessing import Queue, Value
from multiprocessing.synchronize import Event as EventType
from queue import Empty
from time import time_ns
from typing import Dict, List, Optional, Tuple, Union

from psycopg2 import DatabaseError, InterfaceError, ProgrammingError
from psycopg2.extensions import AsIs
from zmq import SUB, SUBSCRIBE, Context

from hyrisecockpit.settings import (
    STORAGE_HOST,
    STORAGE_PASSWORD,
    STORAGE_PORT,
    STORAGE_USER,
)

from .cursor import PoolCursor, StorageCursor


def handle_published_data(published_data: Dict, task_queue: Queue) -> None:
    """Fill task queue."""
    tasks = published_data["body"]["querylist"]
    for task in tasks:
        task_queue.put(task)


def fill_queue(
    workload_publisher_url: str,
    task_queue: Queue,
    continue_execution_flag: Value,
    worker_wait_for_exit_event: EventType,
) -> None:
    """Fill the queue."""
    context = Context()
    sub_socket = context.socket(SUB)
    sub_socket.connect(workload_publisher_url)
    sub_socket.setsockopt_string(SUBSCRIBE, "")

    while True:
        published_data: Dict = sub_socket.recv_json()
        if not continue_execution_flag.value:
            worker_wait_for_exit_event.wait()
        else:
            handle_published_data(published_data, task_queue)


def get_formatted_parameters(
    not_formatted_parameters: Tuple[Tuple[Union[str, int], Optional[str]], ...],
) -> Optional[Tuple[Union[AsIs, str], ...]]:
    """Create formatted parameters."""
    if not_formatted_parameters:
        return tuple(
            AsIs(parameter) if protocol == "as_is" else parameter
            for parameter, protocol in not_formatted_parameters
        )
    return None


def execute_task(
    cursor: PoolCursor, query: str, formatted_parameters: Optional[Tuple[str, ...]]
) -> Tuple[int, int]:
    """Execute given task."""
    startts = time_ns()
    cursor.execute(query, formatted_parameters)
    endts = time_ns()

    return endts, endts - startts


def log_results(
    log: StorageCursor,
    last_batched: int,
    succesful_queries: List[Tuple[int, int, str, str, str]],
    failed_queries: List[Tuple[int, str, str, str]],
) -> int:
    """Log results to database."""
    if last_batched < time_ns() - 1_000_000_000:
        log.log_queries(succesful_queries)
        succesful_queries.clear()
        log.log_failed_queries(failed_queries)
        failed_queries.clear()
        return time_ns()
    return last_batched


def execute_queries(
    worker_id: str,
    task_queue: Queue,
    cur: PoolCursor,
    continue_execution_flag: Value,
    database_id: str,
    i_am_done_event: EventType,
    worker_wait_for_exit_event: EventType,
) -> None:
    """Define workers work loop."""
    with cur:
        with StorageCursor(
            STORAGE_HOST, STORAGE_PORT, STORAGE_USER, STORAGE_PASSWORD, database_id
        ) as log:
            succesful_queries: List[Tuple[int, int, str, str, str]] = []
            failed_queries: List[Tuple[int, str, str, str]] = []
            last_batched = time_ns()
            while True:
                if not continue_execution_flag.value:
                    i_am_done_event.set()
                    worker_wait_for_exit_event.wait()

                try:
                    task: Tuple[
                        str, Tuple[Tuple[Union[str, int], Optional[str]], ...], str, str
                    ] = task_queue.get(block=False)
                    query, not_formatted_parameters, workload_type, query_type = task
                    query = query.replace("[STREAM_ID]", str(worker_id))
                    formatted_parameters = get_formatted_parameters(
                        not_formatted_parameters
                    )
                    endts, latency = execute_task(cur, query, formatted_parameters)
                    succesful_queries.append(
                        (endts, latency, workload_type, query_type, worker_id)
                    )
                except Empty:
                    continue
                except (
                    ValueError,
                    ProgrammingError,
                    DatabaseError,
                    InterfaceError,
                ) as e:
                    failed_queries.append((time_ns(), worker_id, str(task), str(e)))

                last_batched = log_results(
                    log, last_batched, succesful_queries, failed_queries
                )
