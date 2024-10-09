from __future__ import annotations

import os
import re
import subprocess
import tempfile
import time
from datetime import datetime
from pathlib import Path
from subprocess import check_call, check_output

import pytest
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


class BaseK8STest:
    """Base class for K8S Tests."""
    host: str = KUBERNETES_HOST_PORT
    temp_dir = Path(tempfile.gettempdir())  # Refers to global temp directory, in linux it usual "/tmp"
    session: requests.Session
    test_id: str
    @pytest.fixture(autouse=True)
    def base_tests_setup(self, request):
        # Replacement for unittests.TestCase.id()
        self.test_id = f"{request.node.cls.__name__}_{request.node.name}"
        self.session = self._get_session_with_retries()
        try:
            self._ensure_airflow_webserver_is_healthy()
            yield
        finally:
            self.session.close()