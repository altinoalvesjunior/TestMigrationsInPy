import os
import sys
import time
import pytest
from unittest.mock import patch

def test_get_ray_wheels_url(remove_buildkite_env):
    url = get_ray_wheels_url(
        repo_url="https://github.com/ray-project/ray.git",
        branch="master",
        commit="1234",
        ray_version="3.0.0.dev0",
    )
    assert (
        url == "https://s3-us-west-2.amazonaws.com/ray-wheels/master/1234/"
        "ray-3.0.0.dev0-cp37-cp37m-manylinux2014_x86_64.whl"
    )