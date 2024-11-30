import datetime

from mock import Mock, patch
from pytest import raises
from sqlalchemy.exc import OperationalError

from airflow.executors.sequential_executor import SequentialExecutor
from airflow.jobs.base_job import BaseJob
from airflow.utils import timezone
from airflow.utils.state import State

class MockJob(BaseJob):
    class TestBaseJob:
        def test_is_alive(self):
            job = MockJob(None, heartrate=10, state=State.RUNNING)
            assert job.is_alive() is True

            job.latest_heartbeat = timezone.utcnow() - datetime.timedelta(seconds=20)
            assert job.is_alive() is True

            job.latest_heartbeat = timezone.utcnow() - datetime.timedelta(seconds=21)
            assert job.is_alive() is False

            # test because .seconds was used before instead of total_seconds
            # internal repr of datetime is (days, seconds)
            job.latest_heartbeat = timezone.utcnow() - datetime.timedelta(days=1)
            assert job.is_alive() is False

            job.state = State.SUCCESS
            job.latest_heartbeat = timezone.utcnow() - datetime.timedelta(seconds=10)
            assert job.is_alive() is False, "Completed jobs even with recent heartbeat should not be alive"