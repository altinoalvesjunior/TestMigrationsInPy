import datetime
import unittest

from mock import Mock, patch
from sqlalchemy.exc import OperationalError

from airflow.executors.sequential_executor import SequentialExecutor
from airflow.jobs.base_job import BaseJob
from airflow.utils.state import State

class TestBaseJob(unittest.TestCase):
    class TestJob(BaseJob):
        def test_state_success(self):
            job = self.TestJob(lambda: True)
            job.run()

            self.assertEqual(job.state, State.SUCCESS)
            self.assertIsNotNone(job.end_date)