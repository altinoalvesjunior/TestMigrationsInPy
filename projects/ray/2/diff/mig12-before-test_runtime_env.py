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
@pytest.mark.parametrize("client_mode", [True, False])
def test_two_node_uri(two_node_cluster, working_dir, client_mode):
    cluster, _ = two_node_cluster
    (address, env, PKG_DIR) = start_client_server(cluster, client_mode)
    import ray._private.runtime_env as runtime_env
    import tempfile
    with tempfile.NamedTemporaryFile(suffix="zip") as tmp_file:
        pkg_name = runtime_env.get_project_package_name(working_dir, [], [])
        pkg_uri = runtime_env.Protocol.PIN_GCS.value + "://" + pkg_name
        runtime_env.create_project_package(working_dir, [], [], tmp_file.name)
        runtime_env.push_package(pkg_uri, tmp_file.name)
        runtime_env = f"""{{ "uris": ["{pkg_uri}"] }}"""
        # Execute the following cmd in driver with runtime_env
        execute_statement = "print(sum(ray.get([run_test.remote()] * 1000)))"
    script = driver_script.format(**locals())
    out = run_string_as_driver(script, env)
    assert out.strip().split()[-1] == "1000"
    assert len(list(Path(PKG_DIR).iterdir())) == 1
    # pinned uri will not be deleted
    print(list(kv._internal_kv_list("")))
    assert len(kv._internal_kv_list("pingcs://")) == 1