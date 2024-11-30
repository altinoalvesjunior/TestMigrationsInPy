import datetime
import os
import shutil
import unittest
from datetime import timedelta
from tempfile import mkdtemp
from unittest import mock
from unittest.mock import MagicMock, patch
from zipfile import ZipFile

import psutil
import pytest
from freezegun import freeze_time
from parameterized import parameterized
from sqlalchemy import func

import airflow.example_dags
import airflow.smart_sensor_dags
from airflow import settings
from airflow.jobs.scheduler_job import SchedulerJob
from airflow.models import DAG, DagBag, DagModel, Pool, TaskInstance, errors
from airflow.operators.dummy import DummyOperator
from airflow.serialization.serialized_objects import SerializedDAG
from airflow.utils import timezone
from airflow.utils.state import State
from airflow.utils.types import DagRunType
from tests.test_utils.config import conf_vars, env_vars


ROOT_FOLDER = os.path.realpath(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, os.pardir)
)
PERF_DAGS_FOLDER = os.path.join(ROOT_FOLDER, "tests", "test_utils", "perf", "dags")
ELASTIC_DAG_FILE = os.path.join(PERF_DAGS_FOLDER, "elastic_dag.py")

TEST_DAG_FOLDER = os.environ['AIRFLOW__CORE__DAGS_FOLDER']
DEFAULT_DATE = timezone.datetime(2016, 1, 1)
TRY_NUMBER = 1
# Include the words "airflow" and "dag" in the file contents,
# tricking airflow into thinking these
# files contain a DAG (otherwise Airflow will skip them)
PARSEABLE_DAG_FILE_CONTENTS = '"airflow DAG"'
UNPARSEABLE_DAG_FILE_CONTENTS = 'airflow DAG'
INVALID_DAG_WITH_DEPTH_FILE_CONTENTS = "def something():\n    return airflow_DAG\nsomething()"

# Filename to be used for dags that are created in an ad-hoc manner and can be removed/
# created at runtime
TEMP_DAG_FILENAME = "temp_dag.py"


@pytest.fixture(scope="class")
def disable_load_example():
    with conf_vars({('core', 'load_examples'): 'false'}):
        with env_vars({('core', 'load_examples'): 'false'}):
            yield


@pytest.mark.usefixtures("disable_load_example")
class TestSchedulerJob(unittest.TestCase):
    def test_execute_task_instances_unlimited(self):
        """Test that max_tis_per_query=0 is unlimited"""

        dag_id = 'SchedulerJobTest.test_execute_task_instances_unlimited'
        task_id_1 = 'dummy_task'
        task_id_2 = 'dummy_task_2'

        dag = DAG(dag_id=dag_id, start_date=DEFAULT_DATE, max_active_tasks=1024)
        task1 = DummyOperator(dag=dag, task_id=task_id_1)
        task2 = DummyOperator(dag=dag, task_id=task_id_2)
        dag = SerializedDAG.from_dict(SerializedDAG.to_dict(dag))

        self.scheduler_job = SchedulerJob(subdir=os.devnull)
        session = settings.Session()

        dag_model = DagModel(
            dag_id=dag_id,
            is_paused=False,
            max_active_tasks=dag.max_active_tasks,
            has_task_concurrency_limits=False,
        )
        session.add(dag_model)
        date = dag.start_date
        tis = []
        for _ in range(0, 20):
            dr = dag.create_dagrun(
                run_type=DagRunType.SCHEDULED,
                execution_date=date,
                state=State.RUNNING,
            )
            date = dag.following_schedule(date)
            ti1 = TaskInstance(task1, dr.execution_date)
            ti2 = TaskInstance(task2, dr.execution_date)
            tis.append(ti1)
            tis.append(ti2)
            ti1.refresh_from_db()
            ti2.refresh_from_db()
            ti1.state = State.SCHEDULED
            ti2.state = State.SCHEDULED
            session.merge(ti1)
            session.merge(ti2)
            session.flush()
        self.scheduler_job.max_tis_per_query = 0
        self.scheduler_job.executor = MagicMock(slots_available=36)

        res = self.scheduler_job._critical_section_execute_task_instances(session)
        # 20 dag runs * 2 tasks each = 40, but limited by number of slots available
        self.assertEqual(36, res)
        session.rollback()