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
    @pytest.mark.backend("postgres", "mysql")
    @parameterized.expand(
        [
            [
                "example_branch_operator",
                (
                    "run_this_first",
                    "branching",
                    "branch_a",
                    "branch_b",
                    "branch_c",
                    "branch_d",
                    "follow_branch_a",
                    "follow_branch_b",
                    "follow_branch_c",
                    "follow_branch_d",
                    "join",
                ),
            ],
            [
                "miscellaneous_test_dag",
                ("runme_0", "runme_1", "runme_2", "also_run_this", "run_after_loop", "run_this_last"),
            ],
            [
                "example_skip_dag",
                (
                    "always_true_1",
                    "always_true_2",
                    "skip_operator_1",
                    "skip_operator_2",
                    "all_success",
                    "one_success",
                    "final_1",
                    "final_2",
                ),
            ],
            ["latest_only", ("latest_only", "task1")],
        ]
    )
    def test_backfill_examples(self, dag_id, expected_execution_order):
        """
        Test backfilling example dags
        Try to backfill some of the example dags. Be careful, not all dags are suitable
        for doing this. For example, a dag that sleeps forever, or does not have a
        schedule won't work here since you simply can't backfill them.
        """
        dag = self.dagbag.get_dag(dag_id)

        logger.info('*** Running example DAG: %s', dag.dag_id)
        executor = MockExecutor()
        job = BackfillJob(
            dag=dag,
            start_date=DEFAULT_DATE,
            end_date=DEFAULT_DATE,
            executor=executor,
            ignore_first_depends_on_past=True,
        )

        job.run()
        assert [
            ((dag_id, task_id, DEFAULT_DATE, 1), (State.SUCCESS, None))
            for task_id in expected_execution_order
        ] == executor.sorted_tasks

    def test_backfill_conf(self):
        dag = self._get_dummy_dag('test_backfill_conf')

        executor = MockExecutor()

        conf_ = json.loads("""{"key": "value"}""")
        job = BackfillJob(
            dag=dag,
            executor=executor,
            start_date=DEFAULT_DATE,
            end_date=DEFAULT_DATE + datetime.timedelta(days=2),
            conf=conf_,
        )
        job.run()

        dr = DagRun.find(dag_id='test_backfill_conf')

        assert conf_ == dr[0].conf