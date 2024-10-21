import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from ray_release.result import ExitCode


class RunScriptTest(unittest.TestCase):
    def testRepeat(self):
        self.assertEquals(
            self._run(ExitCode.SUCCESS, ExitCode.SUCCESS, ExitCode.SUCCESS),
            ExitCode.SUCCESS.value,
        )
        self.assertEquals(self._read_state(), 1)

        self.assertEquals(
            self._run(ExitCode.RAY_WHEELS_TIMEOUT, ExitCode.SUCCESS, ExitCode.SUCCESS),
            ExitCode.SUCCESS.value,
        )
        self.assertEquals(self._read_state(), 2)
        self.assertEquals(
            self._run(
                ExitCode.RAY_WHEELS_TIMEOUT,
                ExitCode.CLUSTER_ENV_BUILD_TIMEOUT,
                ExitCode.SUCCESS,
            ),
            ExitCode.SUCCESS.value,
        )
        self.assertEquals(self._read_state(), 3)
        self.assertEquals(
            self._run(
                ExitCode.CLUSTER_STARTUP_TIMEOUT,
                ExitCode.CLUSTER_WAIT_TIMEOUT,
                ExitCode.RAY_WHEELS_TIMEOUT,
            ),
            ExitCode.RAY_WHEELS_TIMEOUT.value,
        )
        self.assertEquals(self._read_state(), 3)
        self.assertEquals(
            self._run(
                ExitCode.RAY_WHEELS_TIMEOUT, ExitCode.COMMAND_ALERT, ExitCode.SUCCESS
            ),
            ExitCode.COMMAND_ALERT.value,
        )
        self.assertEquals(self._read_state(), 2)