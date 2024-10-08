import multiprocessing
import os
import subprocess
import time
import unittest

import ray

from ray.test.test_utils import run_and_get_output


class MonitorTest(unittest.TestCase):
    @unittest.skipIf(
        os.environ.get("RAY_USE_NEW_GCS", False),
        "Failing with the new GCS API.")
    def testCleanupOnDriverExitSingleRedisShard(self):
        self._testCleanupOnDriverExit(num_redis_shards=1)