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
    def test_round_time(self):
        rt1 = round_time(datetime(2015, 1, 1, 6), timedelta(days=1))
        self.assertEqual(datetime(2015, 1, 1, 0, 0), rt1)
        rt2 = round_time(datetime(2015, 1, 2), relativedelta(months=1))
        self.assertEqual(datetime(2015, 1, 1, 0, 0), rt2)
        rt3 = round_time(datetime(2015, 9, 16, 0, 0), timedelta(1), datetime(2015, 9, 14, 0, 0))
        self.assertEqual(datetime(2015, 9, 16, 0, 0), rt3)
        rt4 = round_time(datetime(2015, 9, 15, 0, 0), timedelta(1), datetime(2015, 9, 14, 0, 0))
        self.assertEqual(datetime(2015, 9, 15, 0, 0), rt4)
        rt5 = round_time(datetime(2015, 9, 14, 0, 0), timedelta(1), datetime(2015, 9, 14, 0, 0))
        self.assertEqual(datetime(2015, 9, 14, 0, 0), rt5)
        rt6 = round_time(datetime(2015, 9, 13, 0, 0), timedelta(1), datetime(2015, 9, 14, 0, 0))
        self.assertEqual(datetime(2015, 9, 14, 0, 0), rt6)