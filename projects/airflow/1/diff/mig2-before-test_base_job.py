import datetime
import unittest

from mock import Mock, patch
from sqlalchemy.exc import OperationalError

from airflow.executors.sequential_executor import SequentialExecutor
from airflow.jobs.base_job import BaseJob
from airflow.utils import timezone
from airflow.utils.session import create_session
from airflow.utils.state import State
from tests.test_utils.config import conf_vars


class TestBaseJob(unittest.TestCase):
    class TestJob(BaseJob):
        def test_state_sysexit(self):
            import sys
            job = self.TestJob(lambda: sys.exit(0))
            job.run()

            self.assertEqual(job.state, State.SUCCESS)
            self.assertIsNotNone(job.end_date)