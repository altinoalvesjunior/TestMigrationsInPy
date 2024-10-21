import json
import os
import subprocess
import sys
import tempfile
import pytest

from ray_release.result import ExitCode

def test_parameters(setup):
    state_file, test_script = setup
    os.environ["RAY_TEST_SCRIPT"] = "ray_release/tests/_test_catch_args.py"
    argv_file = tempfile.mktemp()
    subprocess.check_call(
        f"{test_script} " f"{argv_file} " f"--smoke-test",
        shell=True,
    )

    with open(argv_file, "rt") as fp:
        data = json.load(fp)

    os.unlink(argv_file)

    assert "--smoke-test" in data