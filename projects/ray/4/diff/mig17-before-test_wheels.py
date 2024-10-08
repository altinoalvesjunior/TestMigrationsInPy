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
    def testMatchingRayWheelsURL(self):
        assert not is_wheels_url_matching_ray_verison(
            f"http://some/location/{get_wheels_filename('3.0.0dev0', (3, 8))}", (3, 7)
        )

        assert not is_wheels_url_matching_ray_verison(
            f"http://some/location/{get_wheels_filename('3.0.0dev0', (3, 7))}", (3, 8)
        )

        assert is_wheels_url_matching_ray_verison(
            f"http://some/location/{get_wheels_filename('3.0.0dev0', (3, 7))}", (3, 7)
        )