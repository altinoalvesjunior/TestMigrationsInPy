import datetime

from mock import Mock, patch
from pytest import raises
from sqlalchemy.exc import OperationalError

from airflow.executors.sequential_executor import SequentialExecutor
from airflow.jobs.base_job import BaseJob
from airflow.utils.state import State


class MockJob(BaseJob):
    class TestBaseJob:
        def test_state_success(self):
            job = MockJob(lambda: True)
            job.run()

            assert job.state == State.SUCCESS
            assert job.end_date is not None