import os
import sys
import time
import pytest
from unittest.mock import patch

def test_get_ray_version(remove_buildkite_env):
    init_file = os.path.join(
        os.path.dirname(__file__), "..", "..", "..", "python", "ray", "__init__.py"
    )
    with open(init_file, "rt") as fp:
        content = [line.encode() for line in fp.readlines()]

    with patch("urllib.request.urlopen", lambda _: content):
        version = get_ray_version(DEFAULT_REPO, commit="fake")
        assert version

    with patch("urllib.request.urlopen", lambda _: []), pytest.raises(
        RayWheelsNotFoundError
    ):
        get_ray_version(DEFAULT_REPO, commit="fake")