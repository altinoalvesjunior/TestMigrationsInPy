import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from ray_release.result import ExitCode


class RunScriptTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.mkdtemp()
        self.state_file = os.path.join(self.tempdir, "state.txt")
        self.test_script = os.path.join(
            os.path.dirname(__file__), "..", "..", "run_release_test.sh"
        )

        os.environ["NO_INSTALL"] = "1"
        os.environ["NO_CLONE"] = "1"
        os.environ["NO_ARTIFACTS"] = "1"
        os.environ["RAY_TEST_SCRIPT"] = "ray_release/tests/_test_run_release_test_sh.py"
        os.environ["OVERRIDE_SLEEP_TIME"] = "0"
        os.environ["MAX_RETRIES"] = "3"