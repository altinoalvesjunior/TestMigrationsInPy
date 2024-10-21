import json
import os
import subprocess
import sys
import tempfile
import pytest

from ray_release.result import ExitCode

def test_repeat(setup):
    state_file, test_script = setup
    assert (
        _run_script(
            test_script,
            state_file,
            ExitCode.SUCCESS,
            ExitCode.SUCCESS,
            ExitCode.SUCCESS,
        )
        == ExitCode.SUCCESS.value
    )
    assert _read_state(state_file) == 1
    assert (
        _run_script(
            test_script,
            state_file,
            ExitCode.RAY_WHEELS_TIMEOUT,
            ExitCode.SUCCESS,
            ExitCode.SUCCESS,
        )
        == ExitCode.SUCCESS.value
    )
    assert _read_state(state_file) == 2
    assert (
        _run_script(
            test_script,
            state_file,
            ExitCode.RAY_WHEELS_TIMEOUT,
            ExitCode.CLUSTER_ENV_BUILD_TIMEOUT,
            ExitCode.SUCCESS,
        )
        == ExitCode.SUCCESS.value
    )
    assert _read_state(state_file) == 3
    assert (
        _run_script(
            test_script,
            state_file,
            ExitCode.CLUSTER_STARTUP_TIMEOUT,
            ExitCode.CLUSTER_WAIT_TIMEOUT,
            ExitCode.RAY_WHEELS_TIMEOUT,
        )
        == ExitCode.RAY_WHEELS_TIMEOUT.value
    )
    assert _read_state(state_file) == 3
    assert (
        _run_script(
            test_script,
            state_file,
            ExitCode.RAY_WHEELS_TIMEOUT,
            ExitCode.COMMAND_ALERT,
            ExitCode.SUCCESS,
        )
        == ExitCode.COMMAND_ALERT.value
    )
    assert _read_state(state_file) == 2