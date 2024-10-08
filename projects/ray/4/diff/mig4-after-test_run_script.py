import json
import os
import subprocess
import sys
import tempfile
import pytest

from ray_release.result import ExitCode

def _read_state(state_file):
    with open(state_file, "rt") as f:
        return int(f.read())