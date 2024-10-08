import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from ray_release.result import ExitCode


class RunScriptTest(unittest.TestCase):
    def testParameters(self):
        os.environ["RAY_TEST_SCRIPT"] = "ray_release/tests/_test_catch_args.py"
        argv_file = tempfile.mktemp()

        subprocess.check_call(
            f"{self.test_script} " f"{argv_file} " f"--smoke-test",
            shell=True,
        )

        with open(argv_file, "rt") as fp:
            data = json.load(fp)

        os.unlink(argv_file)

        self.assertIn("--smoke-test", data)