import sys
import pytest

from ray_release.alerts import (
    handle,
    default,
    # long_running_tests,
    # rllib_tests,
    # tune_tests,
    # xgboost_tests,
)
from ray_release.config import Test
from ray_release.exception import ReleaseTestConfigError, ResultsAlert
from ray_release.result import Result

def test_default_alert():
    test = Test(name="unit_alert_test", alert="default")
    assert default.handle_result(test, Result(status="timeout"))
    assert not default.handle_result(test, Result(status="finished"))