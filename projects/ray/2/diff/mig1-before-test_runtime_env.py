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

@unittest.skipIf(sys.platform == "win32", "Fail to create temp dir.")
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