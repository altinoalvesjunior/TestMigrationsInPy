import os
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

import psutil
import pytest

from airflow import settings
from airflow.cli import cli_parser
from airflow.cli.commands import webserver_command
from airflow.cli.commands.webserver_command import GunicornMonitor
from airflow.utils.cli import setup_locations
from tests.test_utils.config import conf_vars

class TestCliWebServer:
    @pytest.fixture(autouse=True)
    def _make_parser(self):
        self.parser = cli_parser.get_parser()

    @pytest.fixture(autouse=True)
    def _cleanup(self):
        self._check_processes()
        self._clean_pidfiles()

        yield
        self._check_processes(ignore_running=True)
        self._clean_pidfiles()