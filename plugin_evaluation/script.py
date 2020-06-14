"""Prototype of the scenario script."""
from time import sleep, time_ns

from plugin_evaluation.cockpit_management.cockpit import Cockpit
from plugin_evaluation.export.exporter import Exporter
from plugin_evaluation.settings import DATABASE_HOST, DATABASE_PORT
from plugin_evaluation.utils.figlet import intro
from plugin_evaluation.utils.user_interface import DoneStatus, show_bar

database_id = "aptera"
pre_workload_execution_time = 1  # at least 1
workload_execution_time = 15
plugin = "Compression"
benchmark = "tpch_1"

basic_frequency = 300
frequency = 300
aggregation_interval = 1
tag = "Compression (10 + 15 min, 400 MB)"

plugin_settings = {
    "database_id": database_id,
    "plugin_name": "Compression",
    "setting_name": "MemoryBudget",
    "value": "500000000",
}

metrics = [
    "throughput",
    "latency",
    "queue_length",
    "cpu_process_usage",
    "footprint",
    "detailed latency",
    "ram usage",
    "access frequency",
]

#############################################################

print(intro)

try:
    exporter = Exporter(tag, csv_export=True)
    cockpit = Cockpit()  # type: ignore
    cockpit.start()

    show_bar("Starting cockpit...", 3)

    with DoneStatus("Check startup errors..."):
        assert (  # nosec
            not cockpit.has_errors()
        ), f"Error during startup of the cockpit\n {cockpit.get_stderr()}"

    with DoneStatus("Adding database..."):
        response = cockpit.backend.add_database(
            database_id, DATABASE_HOST, DATABASE_PORT
        )
        assert (  # nosec
            response.status_code == 200
        ), f"Couldn't add a database ({response.status_code})"

    with DoneStatus("Waiting default tables to load..."):
        cockpit.backend.wait_for_unblocked_status()

    with DoneStatus("Starting a workload..."):
        response = cockpit.backend.start_workers()
        assert (  # nosec
            response.status_code == 200
        ), f"Couldn't start workers ({response.status_code})"
        response = cockpit.backend.start_workload(benchmark, basic_frequency)
        assert (  # nosec
            response.status_code == 200
        ), f"Couldn't start workload ({response.status_code})"
        cockpit.backend.wait_for_unblocked_status()

        # weights = {    # noqa
        #     "06": 1.0
        # }    # noqa
        # response = cockpit.backend.update_tpch_workload(benchmark, frequency, weights) # noqa
        # assert (  # nosec
        #     response.status_code == 200    # noqa
        # ), f"Couldn't update workload ({response.status_code})"

    startts = time_ns()
    show_bar("Executing pre workload...", pre_workload_execution_time)

    with DoneStatus(f"Activate {plugin} plugin..."):  # noqa
        response = cockpit.backend.activate_plugin(database_id, plugin)  # noqa
        assert (  # nosec
            response.status_code == 200
        ), f"Couldn't activate plugin ({response.status_code})"

    sleep(1.0)

    with DoneStatus(f"Setting {plugin} plugin..."):  # noqa
        response = cockpit.backend.set_plugin_settings(**plugin_settings)  # noqa
        assert (  # nosec
            response.status_code == 200
        ), f"Couldn't set plugin ({response.status_code})"

    show_bar("Executing a workload...", workload_execution_time)

    endts = time_ns()
    sleep(1.0)

    with DoneStatus(f"Deactivate {plugin} plugin..."):  # noqa
        response = cockpit.backend.deactivate_plugin(database_id, plugin)  # noqa
        assert (  # nosec
            response.status_code == 200
        ), f"Couldn't deactivate plugin ({response.status_code})"

    with DoneStatus("Stopping a workload..."):
        response = cockpit.backend.stop_workload(benchmark)
        assert (  # nosec
            response.status_code == 200
        ), f"Couldn't stop workload ({response.status_code})"
        response = cockpit.backend.stop_workers()
        assert (  # nosec
            response.status_code == 200
        ), f"Couldn't stop workers ({response.status_code})"
        cockpit.backend.wait_for_unblocked_status()

    with DoneStatus("Removing the database..."):
        response = cockpit.backend.remove_database(database_id)
        assert (  # nosec
            response.status_code == 200
        ), f"Couldn't remove database ({response.status_code})"

    with DoneStatus("Cockpit shutdown..."):
        cockpit.shutdown()

    show_bar("Prepairing for export...", 3)

    startts = int(startts / 1_000_000_000) * 1_000_000_000
    endts = int(endts / 1_000_000_000) * 1_000_000_000

    with DoneStatus("Exporting plugin log..."):
        exporter.initialize_plugin_log(database_id, startts, endts)

    with DoneStatus("Exporting main metrics..."):
        for metric in metrics:
            exporter.plot_metric(
                metric, database_id, startts, endts, None, aggregation_interval
            )

    with DoneStatus("Exporting access frequency..."):
        exporter.plot_metric_for_benchmark(  # noqa
            "table access frequency",
            benchmark,
            database_id,
            startts,
            endts,
            aggregation_interval,  # noqa
        )  # noqa

    with DoneStatus("Exporting footprint..."):
        exporter.plot_metric_for_benchmark(  # noqa
            "table footprint",
            benchmark,
            database_id,
            startts,
            endts,
            aggregation_interval,  # noqa
        )  # noqa

    with DoneStatus("Exporting query latency..."):
        exporter.plot_query_metric_for_benchmark(  # noqa
            "query latency",
            benchmark,
            database_id,
            startts,
            endts,
            aggregation_interval,  # noqa
        )  # noqa

except KeyboardInterrupt:
    print("\n\U00002757[KEYBOARD INTERRUPT]\U00002757")
    with DoneStatus("Cockpit shutdown..."):
        cockpit.shutdown()

except AssertionError as error:
    print(f"\U0000274C[ERROR]\U0000274C\n{error}")
    with DoneStatus("Cockpit shutdown..."):
        cockpit.shutdown()
