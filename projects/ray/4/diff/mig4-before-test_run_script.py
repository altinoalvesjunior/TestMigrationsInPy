import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from ray_release.result import ExitCode


class RunScriptTest(unittest.TestCase):
    def _read_state(self):
        with open(self.state_file, "rt") as f:
            return int(f.read())