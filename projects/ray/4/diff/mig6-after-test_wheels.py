import os
import sys
import time
import pytest

@pytest.fixture
def remove_buildkite_env():
    for key in os.environ:
        if key.startswith("BUILDKITE"):
            os.environ.pop(key)