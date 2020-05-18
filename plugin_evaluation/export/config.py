"""Module with metric configs."""

from plugin_evaluation.export.aggregation_handling import (
    idle_aggregation,
    time_aggregation,
)
from plugin_evaluation.export.influx_handling import (
    get_detailed_latency_information,
    get_metric_data,
    get_metric_data_with_fill,
    get_query_latency,
    get_ram_usage,
)
from plugin_evaluation.export.plot_handling import plot_bar_chart, plot_line_chart
from plugin_evaluation.export.points_handling import (
    calculate_access_frequency,
    calculate_access_frequency_for_table,
    calculate_footprint,
    calculate_footprint_for_table,
    default_function,
    handle_query_latency,
    ns_to_ms,
    sort_detailed_latency_points,
)

config = {
    "throughput": {
        "table_name": "throughput",
        "column_name": "throughput",
        "x_label": "Time",
        "y_label": "Queries / second",
        "influx_function": get_metric_data_with_fill,
        "points_function": default_function,
        "aggregation_function": time_aggregation,
        "plot_function": plot_line_chart,
        "path": "",
        "log_interval": 1,
    },
    "latency": {
        "table_name": "latency",
        "column_name": "latency",
        "x_label": "Time",
        "y_label": "ms",
        "influx_function": get_metric_data_with_fill,
        "aggregation_function": time_aggregation,
        "points_function": ns_to_ms,
        "plot_function": plot_line_chart,
        "path": "",
        "log_interval": 1,
    },
    "queue_length": {
        "table_name": "queue_length",
        "column_name": "queue_length",
        "x_label": "Time",
        "y_label": "number of items",
        "influx_function": get_metric_data,
        "points_function": default_function,
        "aggregation_function": time_aggregation,
        "plot_function": plot_line_chart,
        "path": "",
        "log_interval": 1,
    },
    "cpu_process_usage": {
        "table_name": "system_data",
        "column_name": "cpu_process_usage",
        "x_label": "Time",
        "y_label": "% usage",
        "influx_function": get_metric_data,
        "points_function": default_function,
        "aggregation_function": time_aggregation,
        "plot_function": plot_line_chart,
        "path": "",
        "log_interval": 1,
    },
    "ram usage": {
        "table_name": "system_data",
        "column_name": "used_memory",
        "x_label": "Time",
        "y_label": "MB",
        "influx_function": get_ram_usage,
        "points_function": ns_to_ms,
        "aggregation_function": time_aggregation,
        "plot_function": plot_line_chart,
        "path": "",
        "log_interval": 1,
    },
    "footprint": {
        "table_name": "storage",
        "column_name": "storage_meta_information",
        "x_label": "Time",
        "y_label": "MB",
        "influx_function": get_metric_data,
        "points_function": calculate_footprint,
        "aggregation_function": time_aggregation,
        "plot_function": plot_line_chart,
        "path": "",
        "log_interval": 5,
    },
    "table footprint": {
        "table_name": "storage",
        "column_name": "storage_meta_information",
        "x_label": "Time",
        "y_label": "MB",
        "influx_function": get_metric_data,
        "points_function": calculate_footprint_for_table,
        "aggregation_function": time_aggregation,
        "plot_function": plot_line_chart,
        "path": "Footprint/",
        "log_interval": 5,
    },
    "table access frequency": {
        "table_name": "chunks_data",
        "column_name": "chunks_data_meta_information",
        "x_label": "Time",
        "y_label": "Number of accesses",
        "influx_function": get_metric_data,
        "points_function": calculate_access_frequency_for_table,
        "aggregation_function": time_aggregation,
        "plot_function": plot_line_chart,
        "path": "Access frequency/",
        "log_interval": 5,
    },
    "access frequency": {
        "table_name": "chunks_data",
        "column_name": "chunks_data_meta_information",
        "x_label": "Time",
        "y_label": "Number of accesses",
        "influx_function": get_metric_data,
        "points_function": calculate_access_frequency,
        "aggregation_function": time_aggregation,
        "plot_function": plot_line_chart,
        "path": "",
        "log_interval": 5,
    },
    "detailed latency": {
        "table_name": "successful_queries",  # ignored
        "column_name": "latency",  # ignored
        "x_label": "Time",
        "y_label": "ms",
        "influx_function": get_detailed_latency_information,
        "points_function": sort_detailed_latency_points,
        "aggregation_function": idle_aggregation,
        "plot_function": plot_bar_chart,
        "path": "",
        "log_interval": 1,
    },
    "query latency": {
        "table_name": "successful_queries",
        "column_name": "query_latency",
        "x_label": "Time",
        "y_label": "ms",
        "influx_function": get_query_latency,
        "points_function": handle_query_latency,
        "aggregation_function": time_aggregation,
        "plot_function": plot_line_chart,
        "path": "Query latency/",
        "log_interval": 1,
    },
}
