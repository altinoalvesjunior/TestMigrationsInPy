from __future__ import annotations

import contextlib
import json
import logging
import os
import re
import shutil
import sys

from argparse import ArgumentParser
from contextlib import contextmanager, redirect_stdout
from io import StringIO
from pathlib import Path
from typing import TYPE_CHECKING
from unittest import mock
from unittest.mock import sentinel

import pendulum
import pytest
import sqlalchemy.exc

from airflow.cli import cli_parser
from airflow.cli.commands import task_command
from airflow.cli.commands.task_command import LoggerMutationHelper
from airflow.configuration import conf
from airflow.exceptions import AirflowException, DagRunNotFound
from airflow.models import DagBag, DagRun, Pool, TaskInstance
from airflow.models.serialized_dag import SerializedDagModel
from airflow.operators.bash import BashOperator
from airflow.utils import timezone
from airflow.utils.session import create_session
from airflow.utils.state import State
from airflow.utils.types import DagRunType
from tests.test_utils.config import conf_vars
from tests.test_utils.db import clear_db_pools, clear_db_runs

pytestmark = pytest.mark.db_test

class TestLogsfromTaskRunCommand:
    @pytest.mark.skipif(not hasattr(os, "fork"), reason="Forking not available")
    def test_logging_with_run_task(self):
        with conf_vars({("core", "dags_folder"): self.dag_path}):
            task_command.task_run(self.parser.parse_args(self.task_args))

        with open(self.ti_log_file_path) as l_file:
            logs = l_file.read()

        print(logs)  # In case of a test failures this line would show detailed log
        logs_list = logs.splitlines()

        assert "INFO - Started process" in logs
        assert f"Subtask {self.task_id}" in logs
        assert "standard_task_runner.py" in logs
        assert (
            f"INFO - Running: ['airflow', 'tasks', 'run', '{self.dag_id}', "
            f"'{self.task_id}', '{self.run_id}'," in logs
        )

        self.assert_log_line("Log from DAG Logger", logs_list)
        self.assert_log_line("Log from TI Logger", logs_list)
        self.assert_log_line("Log from Print statement", logs_list, expect_from_logging_mixin=True)

        assert (
            f"INFO - Marking task as SUCCESS. dag_id={self.dag_id}, "
            f"task_id={self.task_id}, execution_date=20170101T000000" in logs
        )