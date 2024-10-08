import json
import os
import subprocess
import sys
import tempfile
import pytest

from ray_release.result import ExitCode

def _run_script(test_script, state_file, *exits):
    assert len(exits) == 3
    if os.path.exists(state_file):
        os.unlink(state_file)
    try:
        return subprocess.check_call(
            f"{test_script} "
            f"{state_file} "
            f"{' '.join(str(e.value) for e in exits)}",
            shell=True,
        )
    except subprocess.CalledProcessError as e:
        return e.returncode