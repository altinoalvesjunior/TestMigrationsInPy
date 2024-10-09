import json
import os
import subprocess
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

class TestCliWebServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = cli_parser.get_parser()

    def setUp(self) -> None:
        self._check_processes()
        self._clean_pidfiles()
    
    def tearDown(self) -> None:
        self._check_processes(ignore_running=True)
        self._clean_pidfiles()