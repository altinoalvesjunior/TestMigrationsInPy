import datetime
import json
import logging
import threading
import unittest
from unittest.mock import patch

import pytest
import sqlalchemy
from parameterized import parameterized

from airflow import settings
from airflow.cli import cli_parser
from airflow.exceptions import (
    AirflowException,
    AirflowTaskTimeout,
    BackfillUnfinished,
    DagConcurrencyLimitReached,
    NoAvailablePoolSlot,
    TaskConcurrencyLimitReached,
)
from airflow.jobs.backfill_job import BackfillJob
from airflow.models import DAG, DagBag, Pool, TaskInstance as TI
from airflow.models.dagrun import DagRun
from airflow.models.taskinstance import TaskInstanceKey
from airflow.operators.dummy import DummyOperator
from airflow.utils import timezone
from airflow.utils.session import create_session
from airflow.utils.state import State
from airflow.utils.timeout import timeout
from airflow.utils.types import DagRunType
from tests.test_utils.db import clear_db_pools, clear_db_runs, set_default_pool_slots
from tests.test_utils.mock_executor import MockExecutor

logger = logging.getLogger(__name__)

DEFAULT_DATE = timezone.datetime(2016, 1, 1)


class TestBackfillJob(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dagbag = DagBag(include_examples=True)