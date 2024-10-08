import os
import pytest
import sys
import unittest
import random
import tempfile
import requests
from pathlib import Path
import ray

from ray.test_utils import (
    run_string_as_driver, run_string_as_driver_nonblocking, get_wheel_filename,
    get_master_wheel_url, get_release_wheel_url)
import ray.experimental.internal_kv as kv
from time import sleep

driver_script = """
from time import sleep
import sys
import logging
sys.path.insert(0, "{working_dir}")
import ray
import ray.util
import os
try:
    import test_module
except:
    pass
job_config = ray.job_config.JobConfig(
    runtime_env={runtime_env}
)
if not job_config.runtime_env:
    job_config=None
try:
    if os.environ.get("USE_RAY_CLIENT"):
        ray.util.connect("{address}", job_config=job_config, namespace="")
    else:
        ray.init(address="{address}",
                 job_config=job_config,
                 logging_level=logging.DEBUG,
                 namespace=""
)
except ValueError:
    print("ValueError")
    sys.exit(0)
except TypeError:
    print("TypeError")
    sys.exit(0)
except:
    print("ERROR")
    sys.exit(0)
if os.environ.get("EXIT_AFTER_INIT"):
    sys.exit(0)
@ray.remote
def run_test():
    return test_module.one()
@ray.remote
def check_file(name):
    try:
        with open(name) as f:
            return f.read()
    except:
        return "FAILED"
@ray.remote
class TestActor(object):
    @ray.method(num_returns=1)
    def one(self):
        return test_module.one()
{execute_statement}
if os.environ.get("USE_RAY_CLIENT"):
    ray.util.disconnect()
else:
    ray.shutdown()
sleep(10)
"""

@unittest.skipIf(sys.platform == "win32", "Fail to create temp dir.")
def test_init(shutdown_only):
    with tempfile.TemporaryDirectory() as tmp_dir:
        old_dir = os.getcwd()
        os.chdir(tmp_dir)
        with open("hello", "w") as f:
            f.write("world")
        job_config = ray.job_config.JobConfig(runtime_env={"working_dir": "."})
        ray.init(job_config=job_config)

        @ray.remote
        class Test:
            def test(self):
                with open("hello") as f:
                    return f.read()

        t = Test.remote()
        assert ray.get(t.test.remote()) == "world"
        os.chdir(old_dir)