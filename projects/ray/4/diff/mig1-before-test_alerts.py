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
    def testHandleAlert(self):
        # Unknown test suite
        with self.assertRaises(ReleaseTestConfigError):
            handle.handle_result(
                Test(name="unit_alert_test", alert="invalid"), Result(status="finished")
            )
        # Alert raised
        with self.assertRaises(ResultsAlert):
            handle.handle_result(
                Test(name="unit_alert_test", alert="default"),
                Result(status="unsuccessful"),
            )

        # Everything fine
        handle.handle_result(
            Test(name="unit_alert_test", alert="default"), Result(status="finished")
        )