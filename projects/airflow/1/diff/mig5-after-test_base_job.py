import datetime

from mock import Mock, patch
from pytest import raises
from sqlalchemy.exc import OperationalError

from airflow.executors.sequential_executor import SequentialExecutor
from airflow.jobs.base_job import BaseJob
from airflow.utils.state import State
from tests.test_utils.config import conf_vars


class MockJob(BaseJob):
    class TestBaseJob:
        @conf_vars({('scheduler', 'max_tis_per_query'): '100'})
        @patch('airflow.jobs.base_job.ExecutorLoader.get_default_executor')
        @patch('airflow.jobs.base_job.get_hostname')
        @patch('airflow.jobs.base_job.getpass.getuser')
        def test_essential_attr(self, mock_getuser, mock_hostname, mock_default_executor):
            mock_sequential_executor = SequentialExecutor()
            mock_hostname.return_value = "test_hostname"
            mock_getuser.return_value = "testuser"
            mock_default_executor.return_value = mock_sequential_executor

            test_job = MockJob(None, heartrate=10, dag_id="example_dag", state=State.RUNNING)
            assert test_job.executor_class == "SequentialExecutor"
            assert test_job.heartrate == 10
            assert test_job.dag_id == "example_dag"
            assert test_job.hostname == "test_hostname"
            assert test_job.max_tis_per_query == 100
            assert test_job.unixname == "testuser"
            assert test_job.state == "running"
            assert test_job.executor == mock_sequential_executor
