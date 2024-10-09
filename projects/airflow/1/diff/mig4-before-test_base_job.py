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
        def test_most_recent_job(self):
            with create_session() as session:
                old_job = self.TestJob(None, heartrate=10)
                old_job.latest_heartbeat = old_job.latest_heartbeat - datetime.timedelta(seconds=20)
                job = self.TestJob(None, heartrate=10)
                session.add(job)
                session.add(old_job)
                session.flush()

                self.assertEqual(
                    self.TestJob.most_recent_job(session=session),
                    job
                )

                session.rollback()