from hyrisecockpit.api.app.monitor.service import MonitorService
from hyrisecockpit.api.app.monitor.model import TimeInterval, SystemEntry
from unittest.mock import MagicMock
from typing import Type, Dict, List
from pytest import fixture
from unittest.mock import patch


class TestMonitorService:
    """Tests for the monitor service."""

    @fixture
    def monitor_service(self) -> Type[MonitorService]:
        """Get a MonitorService class without IPC."""
        return MonitorService

    @patch("hyrisecockpit.api.app.monitor.service.get_interval_limits")
    @patch("hyrisecockpit.api.app.monitor.service.get_historical_metric")
    @patch("hyrisecockpit.api.app.monitor.service.StorageConnection")
    def test_get_data_for_time_intervall(
        self,
        mock_storage_connection: MagicMock,
        mock_get_historical_metric: MagicMock,
        mock_get_interval_limits: MagicMock,
        monitor_service: MonitorService,
    ) -> None:
        """Test get data."""
        fake_time_interval = TimeInterval(startts=42, endts=100, precision=1)
        fake_table_name = "table_name"
        fake_column_names = ["column_one", "column_two"]
        mock_get_interval_limits.return_value = (
            50,
            100,
        )
        mock_get_historical_metric.return_value = "response"

        mock_client: MagicMock = MagicMock()
        mock_storage_connection.return_value.__enter__.return_value = mock_client

        response = monitor_service.get_data(
            fake_time_interval, fake_table_name, fake_column_names
        )

        mock_get_interval_limits.assert_called_once_with(42, 100, 1)
        mock_get_historical_metric.assert_called_once_with(
            50, 100, 1, fake_table_name, fake_column_names, mock_client
        )
        assert response == "response"  # type: ignore

    @patch("hyrisecockpit.api.app.monitor.service._get_active_databases")
    @patch("hyrisecockpit.api.app.monitor.service.StorageConnection")
    def test_gets_failed_tasks(
        self,
        mock_storage_connection: MagicMock,
        mock_get_active_databases: MagicMock,
        monitor_service: MonitorService,
    ) -> None:
        mock_client = MagicMock()
        mock_client.query.return_value = {
            ("failed_queries", None): [
                {
                    "time": "2042-10-10T00:00:00Z",
                    "error": "some_error",
                    "task": "select * from foo",
                    "worker_id": "worker_1",
                },
                {
                    "time": "2050-10-10T00:00:00Z",
                    "error": "some_extra_error",
                    "task": "select * from haha",
                    "worker_id": "worker_2",
                },
            ]
        }
        mock_storage_connection.return_value.__enter__.return_value = mock_client
        mock_get_active_databases.return_value = ["database_id"]
        result = monitor_service.get_failed_tasks()

        assert result[0].id == "database_id"
        assert vars(result[0].failed_task_entries[0]) == {
            "timestamp": "2042-10-10T00:00:00Z",
            "error": "some_error",
            "task": "select * from foo",
            "worker_id": "worker_1",
        }
        assert vars(result[0].failed_task_entries[1]) == {
            "timestamp": "2050-10-10T00:00:00Z",
            "error": "some_extra_error",
            "task": "select * from haha",
            "worker_id": "worker_2",
        }

    def test_gets_system_data(self, monitor_service: MonitorService) -> None:
        entry_point: Dict = {
            "timestamp": 1234,
            "cpu_system_usage": 4.2,
            "cpu_process_usage": 4.5,
            "cpu_count": 16,
            "free_memory": 30,
            "available_memory": 100,
            "total_memory": 50,
            "database_threads": 16,
        }
        system_entry: Dict = {"id": "hallo_world", "system_data": [entry_point]}
        system_data: List[Dict] = [system_entry]
        mock_get_data: MagicMock = MagicMock()
        mock_get_data.return_value = system_data
        monitor_service.get_data = mock_get_data  # type: ignore
        time_interval = TimeInterval(startts=42, endts=100, precision=1)

        expected_cpu_model: Dict = {
            "cpu_system_usage": 4.2,
            "cpu_process_usage": 4.5,
            "cpu_count": 16,
        }
        expected_memory_model: Dict = {
            "free": 30,
            "available": 100,
            "total": 50,
            "percent": 2.0,
        }
        response: List[SystemEntry] = monitor_service.get_system_data(time_interval)

        assert response[0].database_id == "hallo_world"
        assert response[0].system_data[0].timestamp == 1234
        assert vars(response[0].system_data[0].system_data.cpu) == expected_cpu_model
        assert (
            vars(response[0].system_data[0].system_data.memory) == expected_memory_model
        )
        assert response[0].system_data[0].system_data.database_threads == 16

    def test_gets_system_data_if_total_memory_is_zero(
        self, monitor_service: MonitorService
    ) -> None:
        entry_point: Dict = {
            "timestamp": 1234,
            "cpu_system_usage": 4.2,
            "cpu_process_usage": 4.5,
            "cpu_count": 16,
            "free_memory": 30,
            "available_memory": 100,
            "total_memory": 0.0,
            "database_threads": 16,
        }
        system_entry: Dict = {
            "id": "hallo_world",
            "system_data": [entry_point],
        }
        system_data: List[Dict] = [system_entry]
        mock_get_data: MagicMock = MagicMock()
        mock_get_data.return_value = system_data
        monitor_service.get_data = mock_get_data  # type: ignore
        time_interval = TimeInterval(startts=42, endts=100, precision=1)

        expected_cpu_model: Dict = {
            "cpu_system_usage": 4.2,
            "cpu_process_usage": 4.5,
            "cpu_count": 16,
        }
        expected_memory_model: Dict = {
            "free": 30,
            "available": 100,
            "total": 0.0,
            "percent": 0.0,
        }
        response: List[SystemEntry] = monitor_service.get_system_data(time_interval)

        assert response[0].database_id == "hallo_world"
        assert response[0].system_data[0].timestamp == 1234
        assert vars(response[0].system_data[0].system_data.cpu) == expected_cpu_model
        assert (
            vars(response[0].system_data[0].system_data.memory) == expected_memory_model
        )
        assert response[0].system_data[0].system_data.database_threads == 16
