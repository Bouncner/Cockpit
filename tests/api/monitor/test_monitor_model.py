from typing import Dict, List
from hyrisecockpit.api.app.monitor.model import (
    FailedTaskEntry,
    FailedTasks,
    TimeInterval,
    Cpu,
    Memory,
    SystemDataEntry,
    SystemData,
    SystemEntry,
    ChunksEntry,
    EncodingEntry,
    ColumnEntry,
    TableData,
    StorageDataEntry,
    StorageData,
    EncodingTypeEntry,
    OrderModeEntry,
    SegmentConfigurationEntry,
    WorkloadStatementInformationEntry,
    WorkloadStatementInformation,
    WorkloadOperatorInformationEntry,
    WorkloadOperatorInformation,
)


class TestFailedTasksModel:
    def test_creates_failed_task_entry(self):
        timestamp: int = 123456789
        worker_id: str = "worker_01"
        task: str = "select * from foo;"
        error: str = "Table with name foo does not exist."
        failed_task_model: FailedTaskEntry = FailedTaskEntry(
            timestamp=timestamp,
            worker_id=worker_id,
            task=task,
            error=error,
        )
        assert timestamp == failed_task_model.timestamp
        assert worker_id == failed_task_model.worker_id
        assert task == failed_task_model.task
        assert error == failed_task_model.error

    def test_creates_failed_tasks(self):
        database_id: str = "database_id"
        timestamp_failed_one: int = 1
        worker_id_failed_one: str = "worker_01"
        task_failed_one: str = "select * from foo;"
        error_failed_one: str = "Table with name foo does not exist."
        timestamp_failed_two: int = 2
        worker_id_failed_two: str = "worker_02"
        task_failed_two: str = "select * from foo;"
        error_failed_two: str = "Table with name foo does not exist."
        failed_task_model_one: FailedTaskEntry = FailedTaskEntry(
            timestamp=timestamp_failed_one,
            worker_id=worker_id_failed_one,
            task=task_failed_one,
            error=error_failed_one,
        )
        failed_task_model_two: FailedTaskEntry = FailedTaskEntry(
            timestamp=timestamp_failed_two,
            worker_id=worker_id_failed_two,
            task=task_failed_two,
            error=error_failed_two,
        )
        failed_task_model: FailedTasks = FailedTasks(
            database_id=database_id,
            failed_task_entries=[failed_task_model_one, failed_task_model_two],
        )
        assert database_id == failed_task_model.id
        assert [
            failed_task_model_one,
            failed_task_model_two,
        ] == failed_task_model.failed_task_entries


class TestTimeIntervalModel:
    def test_creates_time_interval(self) -> None:
        """A TimeInterval model can be created."""
        assert TimeInterval(
            startts=1,
            endts=2,
            precision=1,
        )


class TestSystemModel:
    def test_creates_cpu_model(self) -> None:
        cpu_system_usage: float = 0.42
        cpu_process_usage: float = 0.12
        cpu_count: int = 32

        cpu_model: Cpu = Cpu(
            cpu_system_usage=cpu_system_usage,
            cpu_process_usage=cpu_process_usage,
            cpu_count=cpu_count,
        )

        assert cpu_model.cpu_system_usage == cpu_system_usage
        assert cpu_model.cpu_process_usage == cpu_process_usage
        assert cpu_model.cpu_count == cpu_count

    def test_creates_memory_model(self) -> None:
        free: int = 1234
        available: int = 6789
        total: int = 90000
        percent: float = 10.42

        memory_model: Memory = Memory(
            free=free, available=available, total=total, percent=percent
        )

        assert memory_model.free == free
        assert memory_model.available == available
        assert memory_model.total == total
        assert memory_model.percent == percent

    def test_creates_system_data_entry_model(self) -> None:
        cpu_model = Cpu(cpu_system_usage=0.42, cpu_process_usage=0.42, cpu_count=16)
        memory_model = Memory(free=10, available=10, total=20, percent=10.2)
        database_threads: int = 10

        system_data_entry_model: SystemDataEntry = SystemDataEntry(
            cpu=cpu_model, memory=memory_model, database_threads=database_threads
        )

        assert system_data_entry_model.cpu == cpu_model
        assert system_data_entry_model.memory == memory_model
        assert system_data_entry_model.database_threads == database_threads

    def test_creates_system_data(self) -> None:
        cpu_model = Cpu(cpu_system_usage=0.42, cpu_process_usage=0.42, cpu_count=16)
        memory_model = Memory(free=10, available=10, total=20, percent=10.2)
        database_threads: int = 10
        system_data_entry_model: SystemDataEntry = SystemDataEntry(
            cpu=cpu_model, memory=memory_model, database_threads=database_threads
        )
        timestamp: int = 42

        sytem_data_model: SystemData = SystemData(
            timestamp=timestamp, system_data_entry=system_data_entry_model
        )

        assert sytem_data_model.timestamp == timestamp
        assert sytem_data_model.system_data == system_data_entry_model

    def test_creates_system_entry(self) -> None:
        cpu_model = Cpu(cpu_system_usage=0.42, cpu_process_usage=0.42, cpu_count=16)
        memory_model = Memory(free=10, available=10, total=20, percent=10.2)
        database_threads: int = 10
        system_data_entry_model: SystemDataEntry = SystemDataEntry(
            cpu=cpu_model, memory=memory_model, database_threads=database_threads
        )
        timestamp: int = 42
        sytem_data_model: SystemData = SystemData(
            timestamp=timestamp, system_data_entry=system_data_entry_model
        )
        database_id: str = "database_one"

        system_entry_model: SystemEntry = SystemEntry(
            database_id=database_id, system_data=[sytem_data_model]
        )

        assert system_entry_model.id == database_id
        assert system_entry_model.system_data[0] == sytem_data_model


class TestChunksModel:
    def test_creates_chunks_entry(self) -> None:
        database_id: str = "database_one"
        chunks_data: Dict = {
            "part_tpch_1": {
                "p_brand": [0, 0, 0, 0],
                "p_comment": [0, 0, 0, 0],
                "p_container": [0, 0, 0, 0],
            }
        }

        chunks_entry_model: ChunksEntry = ChunksEntry(
            database_id=database_id, chunks_data=chunks_data
        )

        assert chunks_entry_model.id == database_id
        assert chunks_entry_model.chunks_data == chunks_data


class TestStorageModel:
    def test_creates_encoding_entry(self) -> None:
        name: str = "Dictionary"
        amount: int = 1
        compression: List[str] = ["FixedSize2ByteAligned"]

        encoding_entry_model: EncodingEntry = EncodingEntry(
            name=name, amount=amount, compression=compression
        )

        assert encoding_entry_model.name == name
        assert encoding_entry_model.amount == amount
        assert encoding_entry_model.compression == compression

    def test_creates_colums_entry(self) -> None:
        size: int = 89644
        data_type: str = "float"
        encoding: List[EncodingEntry] = [
            EncodingEntry(
                name="Dictionary", amount=1, compression=["FixedSize2ByteAligned"]
            )
        ]

        colums_entry_model: ColumnEntry = ColumnEntry(
            size=size, data_type=data_type, encoding=encoding
        )

        assert colums_entry_model.size == size
        assert colums_entry_model.data_type == data_type
        assert colums_entry_model.encoding == encoding

    def test_creates_table_data(self) -> None:
        size: int = 4374976
        number_columns: int = 1
        encoding: List[EncodingEntry] = [
            EncodingEntry(
                name="Dictionary", amount=1, compression=["FixedSize2ByteAligned"]
            )
        ]
        colums_entry_model: ColumnEntry = ColumnEntry(
            size=89644, data_type="float", encoding=encoding
        )
        data: Dict[str, ColumnEntry] = {"c_acctbal": colums_entry_model}

        table_data_model: TableData = TableData(
            size=size, number_columns=number_columns, data=data
        )

        assert table_data_model.size == size
        assert table_data_model.number_columns == number_columns
        assert table_data_model.data == data

    def test_creates_storage_data_entry(self) -> None:
        timestamp: int = 42
        encoding: List[EncodingEntry] = [
            EncodingEntry(
                name="Dictionary", amount=1, compression=["FixedSize2ByteAligned"]
            )
        ]
        colums_entry_model: ColumnEntry = ColumnEntry(
            size=89644, data_type="float", encoding=encoding
        )
        data: Dict[str, ColumnEntry] = {"c_acctbal": colums_entry_model}
        table_data_model: TableData = TableData(
            size=4374976, number_columns=1, data=data
        )

        storage_data_entry_model: StorageDataEntry = StorageDataEntry(
            timestamp=timestamp, table_data={"customer_tpch_0_1": table_data_model}
        )

        assert storage_data_entry_model.timestamp == timestamp
        assert storage_data_entry_model.table_data == {
            "customer_tpch_0_1": table_data_model
        }

    def test_creates_storage_data(self) -> None:
        database_id: str = "some_db_id"
        encoding: List[EncodingEntry] = [
            EncodingEntry(
                name="Dictionary", amount=1, compression=["FixedSize2ByteAligned"]
            )
        ]
        colums_entry_model: ColumnEntry = ColumnEntry(
            size=89644, data_type="float", encoding=encoding
        )
        data: Dict[str, ColumnEntry] = {"c_acctbal": colums_entry_model}
        table_data_model: TableData = TableData(
            size=4374976, number_columns=1, data=data
        )

        storage_data_entry_model: StorageDataEntry = StorageDataEntry(
            timestamp=42, table_data={"customer_tpch_0_1": table_data_model}
        )

        storage_data_model: StorageData = StorageData(
            database_id=database_id, storage=[storage_data_entry_model]
        )

        assert storage_data_model.id == database_id
        assert storage_data_model.storage == [storage_data_entry_model]


class TestSegmentConfigurationModel:
    def test_creates_encoding_entry(self) -> None:
        encoding_type: str = "Dictionary"

        encoding_entry_model: EncodingTypeEntry = EncodingTypeEntry(
            encoding_type=encoding_type
        )

        assert encoding_entry_model.encoding_type == encoding_type

    def test_creates_order_mode_entry(self) -> None:
        order_mode: str = "Ascending"

        order_mode_entry_model: OrderModeEntry = OrderModeEntry(order_mode=order_mode)

        assert order_mode_entry_model.order_mode == order_mode

    def test_creates_segment_configuration_entry(self) -> None:
        database_id: str = "some_db_id"
        encoding_entry_model: EncodingTypeEntry = EncodingTypeEntry(
            encoding_type="Dictionary"
        )
        order_mode_entry_model: OrderModeEntry = OrderModeEntry(order_mode="Ascending")
        encoding_type: Dict[str, Dict[str, EncodingTypeEntry]] = {
            "customer_tpch_1": {"0": encoding_entry_model}
        }
        order_mode: Dict[str, Dict[str, OrderModeEntry]] = {
            "customer_tpch_1": {"0": order_mode_entry_model}
        }

        segment_configuration_entry: SegmentConfigurationEntry = (
            SegmentConfigurationEntry(
                id=database_id,
                encoding_type=encoding_type,
                order_mode=order_mode,
            )
        )

        assert segment_configuration_entry.id == database_id
        assert (
            segment_configuration_entry.encoding_type["customer_tpch_1"]["0"]
            == encoding_entry_model
        )
        assert (
            segment_configuration_entry.order_mode["customer_tpch_1"]["0"]
            == order_mode_entry_model
        )


class TestWorkloadStatementInformation:
    def test_creates_workload_statement_information_entry(self) -> None:
        query_type: str = "SELECT"
        total_latency: int = 9568298895
        total_frequency: int = 1504

        workload_statement_information_entry_model: WorkloadStatementInformationEntry = WorkloadStatementInformationEntry(
            query_type=query_type,
            total_latency=total_latency,
            total_frequency=total_frequency,
        )

        assert workload_statement_information_entry_model.query_type == query_type
        assert workload_statement_information_entry_model.total_latency == total_latency
        assert (
            workload_statement_information_entry_model.total_frequency
            == total_frequency
        )

    def test_creates_workload_statement_information(self) -> None:
        database_id: str = "some_db_id"
        workload_statement_information_entry_model: WorkloadStatementInformationEntry = WorkloadStatementInformationEntry(
            query_type="SELECT", total_latency=9568298895, total_frequency=1504
        )

        workload_statement_information_model: WorkloadStatementInformation = (
            WorkloadStatementInformation(
                id=database_id,
                workload_statement_information_entries=[
                    workload_statement_information_entry_model
                ],
            )
        )

        assert workload_statement_information_model.id == database_id
        assert (
            workload_statement_information_model.workload_statement_information_entries[
                0
            ]
            == workload_statement_information_entry_model
        )


class TestWorkloadOperatorInformation:
    def test_creates_workload_operator_information_entry(self) -> None:
        operator: str = "Alias"
        total_time_ns: int = 9568298895

        workload_operator_information_entry_model: WorkloadOperatorInformationEntry = (
            WorkloadOperatorInformationEntry(
                operator=operator,
                total_time_ns=total_time_ns,
            )
        )

        assert workload_operator_information_entry_model.operator == operator
        assert workload_operator_information_entry_model.total_time_ns == total_time_ns

    def test_creates_workload_operator_information(self) -> None:
        database_id: str = "some_db_id"
        workload_operator_information_entry_model: WorkloadOperatorInformationEntry = (
            WorkloadOperatorInformationEntry(operator="Alias", total_time_ns=9568298895)
        )

        workload_operator_information_model: WorkloadOperatorInformation = (
            WorkloadOperatorInformation(
                id=database_id,
                workload_operator_information_entries=[
                    workload_operator_information_entry_model
                ],
            )
        )

        assert workload_operator_information_model.id == database_id
        assert (
            workload_operator_information_model.workload_operator_information_entries[0]
            == workload_operator_information_entry_model
        )
