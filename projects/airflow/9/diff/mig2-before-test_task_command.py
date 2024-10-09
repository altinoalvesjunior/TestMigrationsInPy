from __future__ import annotations

import contextlib
import json
import logging
import os
import re
import shutil
import sys
import unittest
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
    @unittest.skipIf(not hasattr(os, "fork"), "Forking not available")
    def test_run_task_with_pool(self):
        pool_name = "test_pool_run"

        clear_db_pools()
        with create_session() as session:
            pool = Pool(pool=pool_name, slots=1, include_deferred=False)
            session.add(pool)
            session.commit()

            assert session.query(TaskInstance).filter_by(pool=pool_name).first() is None
            task_command.task_run(self.parser.parse_args([*self.task_args, "--pool", pool_name]))
            assert session.query(TaskInstance).filter_by(pool=pool_name).first() is not None

            session.delete(pool)
            session.commit()