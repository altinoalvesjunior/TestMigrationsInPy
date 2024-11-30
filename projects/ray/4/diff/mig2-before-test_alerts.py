import sys
import unittest

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


class AlertsTest(unittest.TestCase):  
    def testDefaultAlert(self):
        self.assertTrue(default.handle_result(self.test, Result(status="timeout")))
        self.assertFalse(default.handle_result(self.test, Result(status="finished")))