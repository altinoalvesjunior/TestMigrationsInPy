import json
import os
import subprocess
import sys
import tempfile
import pytest

from ray_release.result import ExitCode

@pytest.fixture
def setup(tmpdir):
    state_file = os.path.join(tmpdir, "state.txt")
    test_script = os.path.join(
        os.path.dirname(__file__), "..", "..", "run_release_test.sh"
    )
    os.environ["NO_INSTALL"] = "1"
    os.environ["NO_CLONE"] = "1"
    os.environ["NO_ARTIFACTS"] = "1"
    os.environ["RAY_TEST_SCRIPT"] = "ray_release/tests/_test_run_release_test_sh.py"
    os.environ["OVERRIDE_SLEEP_TIME"] = "0"
    os.environ["MAX_RETRIES"] = "3"
    yield state_file, test_script