import datetime

from mock import Mock, patch
from pytest import raises
from sqlalchemy.exc import OperationalError

from airflow.executors.sequential_executor import SequentialExecutor
from airflow.jobs.base_job import BaseJob
from airflow.utils import timezone
from airflow.utils.session import create_session
from airflow.utils.state import State
from tests.test_utils.config import conf_vars


class MockJob(BaseJob):
    class TestBaseJob:
        def test_state_failed(self):
            def abort():
                raise RuntimeError("fail")

            job = MockJob(abort)
            with raises(RuntimeError):
                job.run()

            assert job.state == State.FAILED
            assert job.end_date is not None
