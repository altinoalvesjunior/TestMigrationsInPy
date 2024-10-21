import os
import sys
import time
import unittest
from unittest.mock import patch

from freezegun import freeze_time

from ray_release.config import Test
from ray_release.template import load_test_cluster_env
from ray_release.exception import RayWheelsNotFoundError, RayWheelsTimeoutError
from ray_release.util import url_exists
from ray_release.wheels import (
    get_ray_version,
    DEFAULT_REPO,
    get_ray_wheels_url,
    find_ray_wheels_url,
    find_and_wait_for_ray_wheels_url,
    is_wheels_url_matching_ray_verison,
    get_wheels_filename,
    maybe_rewrite_wheels_url,
)


class WheelsFinderTest(unittest.TestCase):              
    def testGetRayVersion(self):
        init_file = os.path.join(
            os.path.dirname(__file__), "..", "..", "..", "python", "ray", "__init__.py"
        )
        with open(init_file, "rt") as fp:
            content = [line.encode() for line in fp.readlines()]
        with patch("urllib.request.urlopen", lambda _: content):
            version = get_ray_version(DEFAULT_REPO, commit="fake")
            self.assertTrue(version)
        with patch("urllib.request.urlopen", lambda _: []), self.assertRaises(
            RayWheelsNotFoundError
        ):
            get_ray_version(DEFAULT_REPO, commit="fake")