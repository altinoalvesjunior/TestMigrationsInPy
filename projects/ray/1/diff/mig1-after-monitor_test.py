import multiprocessing
import os
import pytest
import subprocess
import time

import ray

from ray.test.test_utils import run_and_get_output

@pytest.mark.skipif(
    os.environ.get("RAY_USE_NEW_GCS") == "on",
    reason="Hanging with the new GCS API.")
def test_cleanup_on_driver_exit_single_redis_shard():
    _test_cleanup_on_driver_exit(num_redis_shards=1)