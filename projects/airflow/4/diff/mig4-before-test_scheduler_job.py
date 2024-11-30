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
from airflow.jobs.scheduler_job import SchedulerJob
from tests.test_utils.config import conf_vars, env_vars
from tests.test_utils.db import (
    clear_db_dags,
    clear_db_import_errors,
    clear_db_jobs,
    clear_db_pools,
    clear_db_runs,
    clear_db_serialized_dags,
    clear_db_sla_miss,
    set_default_pool_slots,
)
from tests.test_utils.mock_executor import MockExecutor
from tests.test_utils.mock_operators import CustomOperator

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
    @staticmethod
    def clean_db():
        clear_db_runs()
        clear_db_pools()
        clear_db_dags()
        clear_db_sla_miss()
        clear_db_import_errors()
        clear_db_jobs()
        # DO NOT try to run clear_db_serialized_dags() here - this will break the tests
        # The tests expect DAGs to be fully loaded here via setUpClass method below
        
    @mock.patch('airflow.jobs.scheduler_job.DagFileProcessorAgent')
    def test_cleanup_methods_all_called(self, mock_processor_agent):
        """
        Test to make sure all cleanup methods are called when the scheduler loop has an exception
        """
        self.scheduler_job = SchedulerJob(subdir=os.devnull, num_runs=1)
        self.scheduler_job.executor = mock.MagicMock(slots_available=8)
        self.scheduler_job._run_scheduler_loop = mock.MagicMock(side_effect=Exception("oops"))
        mock_processor_agent.return_value.end.side_effect = Exception("double oops")
        self.scheduler_job.executor.end = mock.MagicMock(side_effect=Exception("triple oops"))

        with self.assertRaises(Exception):
            self.scheduler_job.run()

        self.scheduler_job.processor_agent.end.assert_called_once()
        self.scheduler_job.executor.end.assert_called_once()
        mock_processor_agent.return_value.end.reset_mock(side_effect=True)