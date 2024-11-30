import datetime
import unittest

from mock import Mock, patch
from sqlalchemy.exc import OperationalError

from airflow.executors.sequential_executor import SequentialExecutor
from airflow.jobs.base_job import BaseJob
from airflow.utils import timezone
from airflow.utils.state import State

class TestBaseJob(unittest.TestCase):
    class TestJob(BaseJob):
        def test_is_alive(self):
            job = self.TestJob(None, heartrate=10, state=State.RUNNING)
            self.assertTrue(job.is_alive())

            job.latest_heartbeat = timezone.utcnow() - datetime.timedelta(seconds=20)
            self.assertTrue(job.is_alive())

            job.latest_heartbeat = timezone.utcnow() - datetime.timedelta(seconds=21)
            self.assertFalse(job.is_alive())

            # test because .seconds was used before instead of total_seconds
            # internal repr of datetime is (days, seconds)
            job.latest_heartbeat = timezone.utcnow() - datetime.timedelta(days=1)
            self.assertFalse(job.is_alive())

            job.state = State.SUCCESS
            job.latest_heartbeat = timezone.utcnow() - datetime.timedelta(seconds=10)
            self.assertFalse(job.is_alive(), "Completed jobs even with recent heartbeat should not be alive")