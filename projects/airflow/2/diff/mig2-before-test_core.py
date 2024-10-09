import multiprocessing
import os
import signal
import unittest
from datetime import timedelta
from time import sleep

from dateutil.relativedelta import relativedelta
from numpy.testing import assert_array_almost_equal
from airflow import settings
from airflow.exceptions import AirflowException, AirflowTaskTimeout
from airflow.hooks.base import BaseHook
from airflow.jobs.local_task_job import LocalTaskJob
from airflow.models import DagBag, DagRun, TaskFail, TaskInstance
from airflow.models.baseoperator import BaseOperator
from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.check_operator import CheckOperator, ValueCheckOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.settings import Session
from airflow.utils.dates import infer_time_unit, round_time, scale_time_units
from airflow.utils.state import State
from airflow.utils.timezone import datetime
from airflow.utils.types import DagRunType
from tests.test_utils.config import conf_vars
from tests.test_utils.db import clear_db_dags, clear_db_runs

DEV_NULL = '/dev/null'
DEFAULT_DATE = datetime(2015, 1, 1)
TEST_DAG_ID = 'unit_tests'

class TestCore(unittest.TestCase):
    def test_infer_time_unit(self):
        self.assertEqual('minutes', infer_time_unit([130, 5400, 10]))
        self.assertEqual('seconds', infer_time_unit([110, 50, 10, 100]))
        self.assertEqual('hours', infer_time_unit([100000, 50000, 10000, 20000]))
        self.assertEqual('days', infer_time_unit([200000, 100000]))