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
        def test_most_recent_job(self):
            with create_session() as session:
                old_job = MockJob(None, heartrate=10)
                old_job.latest_heartbeat = old_job.latest_heartbeat - datetime.timedelta(seconds=20)
                job = MockJob(None, heartrate=10)
                session.add(job)
                session.add(old_job)
                session.flush()

                assert MockJob.most_recent_job(session=session) == job

                session.rollback()