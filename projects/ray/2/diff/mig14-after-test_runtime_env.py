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
@pytest.mark.parametrize("client_mode", [True, False])
def test_detached_actors(ray_start_cluster_head, working_dir, client_mode):
    cluster = ray_start_cluster_head
    (address, env, PKG_DIR) = start_client_server(cluster, client_mode)
    runtime_env = f"""{{  "working_dir": "{working_dir}" }}"""
    # Execute the following cmd in driver with runtime_env
    execute_statement = """
test_actor = TestActor.options(name="test_actor", lifetime="detached").remote()
print(sum(ray.get([test_actor.one.remote()] * 1000)))
"""
    script = driver_script.format(**locals())
    out = run_string_as_driver(script, env)
    assert out.strip().split()[-1] == "1000"
    # It's a detached actors, so it should still be there
    assert len(kv._internal_kv_list("gcs://")) == 1
    assert len(list(Path(PKG_DIR).iterdir())) == 2
    pkg_dir = [f for f in Path(PKG_DIR).glob("*") if f.is_dir()][0]
    import sys
    sys.path.insert(0, str(pkg_dir))
    test_actor = ray.get_actor("test_actor")
    assert sum(ray.get([test_actor.one.remote()] * 1000)) == 1000
    ray.kill(test_actor)
    from time import sleep
    sleep(5)
    assert len(list(Path(PKG_DIR).iterdir())) == 1
    assert len(kv._internal_kv_list("gcs://")) == 0