import datetime
import unittest

from mock import Mock, patch
from sqlalchemy.exc import OperationalError

from airflow.executors.sequential_executor import SequentialExecutor
from airflow.jobs.base_job import BaseJob
from airflow.utils.state import State
from tests.test_utils.config import conf_vars


class TestBaseJob(unittest.TestCase):
    class TestJob(BaseJob):
        @conf_vars({('scheduler', 'max_tis_per_query'): '100'})
        @patch('airflow.jobs.base_job.ExecutorLoader.get_default_executor')
        @patch('airflow.jobs.base_job.get_hostname')
        @patch('airflow.jobs.base_job.getpass.getuser')
        def test_essential_attr(self, mock_getuser, mock_hostname, mock_default_executor):
            mock_sequential_executor = SequentialExecutor()
            mock_hostname.return_value = "test_hostname"
            mock_getuser.return_value = "testuser"
            mock_default_executor.return_value = mock_sequential_executor

            test_job = self.TestJob(None, heartrate=10, dag_id="example_dag", state=State.RUNNING)
            self.assertEqual(test_job.executor_class, "SequentialExecutor")
            self.assertEqual(test_job.heartrate, 10)
            self.assertEqual(test_job.dag_id, "example_dag")
            self.assertEqual(test_job.hostname, "test_hostname")
            self.assertEqual(test_job.max_tis_per_query, 100)
            self.assertEqual(test_job.unixname, "testuser")
            self.assertEqual(test_job.state, "running")
            self.assertEqual(test_job.executor, mock_sequential_executor)