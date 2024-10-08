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
def test_travel():
    import uuid
    with tempfile.TemporaryDirectory() as tmp_dir:
        dir_paths = set()
        file_paths = set()
        item_num = 0
        excludes = []
        root = Path(tmp_dir) / "test"

        def construct(path, excluded=False, depth=0):
            nonlocal item_num
            path.mkdir(parents=True)
            if not excluded:
                dir_paths.add(str(path))
            if depth > 8:
                return
            if item_num > 500:
                return
            dir_num = random.randint(0, 10)
            file_num = random.randint(0, 10)
            for _ in range(dir_num):
                uid = str(uuid.uuid4()).split("-")[0]
                dir_path = path / uid
                exclud_sub = random.randint(0, 5) == 0
                if not excluded and exclud_sub:
                    excludes.append(str(dir_path.relative_to(root)))
                if not excluded:
                    construct(dir_path, exclud_sub or excluded, depth + 1)
                item_num += 1
            if item_num > 1000:
                return

            for _ in range(file_num):
                uid = str(uuid.uuid4()).split("-")[0]
                with (path / uid).open("w") as f:
                    v = random.randint(0, 1000)
                    f.write(str(v))
                    if not excluded:
                        if random.randint(0, 5) == 0:
                            excludes.append(
                                str((path / uid).relative_to(root)))
                        else:
                            file_paths.add((str(path / uid), str(v)))
                item_num += 1

        construct(root)
        exclude_spec = ray._private.runtime_env._get_excludes(root, excludes)
        visited_dir_paths = set()
        visited_file_paths = set()

        def handler(path):
            if path.is_dir():
                visited_dir_paths.add(str(path))
            else:
                with open(path) as f:
                    visited_file_paths.add((str(path), f.read()))

        ray._private.runtime_env._dir_travel(root, [exclude_spec], handler)
        assert file_paths == visited_file_paths
        assert dir_paths == visited_dir_paths