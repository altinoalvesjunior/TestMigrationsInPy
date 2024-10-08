import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from ray_release.result import ExitCode


class RunScriptTest(unittest.TestCase):
    def _run(self, *exits) -> int:
        assert len(exits) == 3
        if os.path.exists(self.state_file):
            os.unlink(self.state_file)
        try:
            return subprocess.check_call(
                f"{self.test_script} "
                f"{self.state_file} "
                f"{' '.join(str(e.value) for e in exits)}",
                shell=True,
            )
        except subprocess.CalledProcessError as e:
            return e.returncode