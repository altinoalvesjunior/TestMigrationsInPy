import datetime

from mock import Mock, patch
from pytest import raises
from sqlalchemy.exc import OperationalError

from airflow.executors.sequential_executor import SequentialExecutor
from airflow.jobs.base_job import BaseJob
from airflow.utils import timezone
from airflow.utils.session import create_session
from airflow.utils.state import State


class MockJob(BaseJob):
    class TestBaseJob:
        @patch('airflow.jobs.base_job.create_session')
        def test_heartbeat_failed(self, mock_create_session):
            when = timezone.utcnow() - datetime.timedelta(seconds=60)
            with create_session() as session:
                mock_session = Mock(spec_set=session, name="MockSession")
                mock_create_session.return_value.__enter__.return_value = mock_session

                job = MockJob(None, heartrate=10, state=State.RUNNING)
                job.latest_heartbeat = when

                mock_session.commit.side_effect = OperationalError("Force fail", {}, None)

                job.heartbeat()

                assert job.latest_heartbeat == when, "attribute not updated when heartbeat fails"