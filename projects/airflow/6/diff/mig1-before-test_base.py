from __future__ import annotations

import os
import re
import subprocess
import tempfile
import time
import unittest
from datetime import datetime
from pathlib import Path
from subprocess import check_call, check_output

import requests
import requests.exceptions
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

CLUSTER_FORWARDED_PORT = os.environ.get("CLUSTER_FORWARDED_PORT") or "8080"
KUBERNETES_HOST_PORT = (os.environ.get("CLUSTER_HOST") or "localhost") + ":" + CLUSTER_FORWARDED_PORT
EXECUTOR = os.environ.get("EXECUTOR")

print()
print(f"Cluster host/port used: ${KUBERNETES_HOST_PORT}")
print(f"Executor: {EXECUTOR}")
print()


class TestBase(unittest.TestCase):
    def setUp(self):
        self.host = KUBERNETES_HOST_PORT
        self.session = self._get_session_with_retries()
        self._ensure_airflow_webserver_is_healthy()
    def tearDown(self):
        self.session.close()