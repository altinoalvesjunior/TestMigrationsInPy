import os
import pytest
import sys
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

@pytest.mark.skipif(sys.platform == "win32", reason="Fail to create temp dir.")
def test_jobconfig_compatible_3(ray_start_cluster_head, working_dir):
    # start job_config=something
    # start job_config=something else
    cluster = ray_start_cluster_head
    (address, env, PKG_DIR) = start_client_server(cluster, True)
    runtime_env = """{  "py_modules": [test_module.__path__[0]] }"""
    # To make the first one hanging ther
    execute_statement = """
sleep(600)
"""
    script = driver_script.format(**locals())
    proc = run_string_as_driver_nonblocking(script, env)
    sleep(5)
    runtime_env = f"""
{{  "working_dir": test_module.__path__[0] }}"""  # noqa: F541
    # Execute the following cmd in the second one and ensure that
    # it is able to run.
    execute_statement = "print('OK')"
    script = driver_script.format(**locals())
    out = run_string_as_driver(script, env)
    proc.kill()
    proc.wait()
    assert out.strip().split()[-1] == "OK"