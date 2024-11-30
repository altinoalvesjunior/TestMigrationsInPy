import os
import sys
import time
import unittest
from unittest.mock import patch

class WheelsFinderTest(unittest.TestCase):
    def _testFindRayWheelsCheckout(
        self, repo: str, branch: str, commit: str, version: str, search_str: str
    ):
        with patch(
            "ray_release.wheels.get_latest_commits", lambda *a, **kw: [commit]
        ), patch(
            "ray_release.wheels.url_exists", lambda *a, **kw: False
        ), self.assertRaises(
            RayWheelsNotFoundError
        ):
            # Fails because URL does not exist
            find_ray_wheels_url(search_str)
        with patch(
            "ray_release.wheels.get_latest_commits", lambda *a, **kw: [commit]
        ), patch("ray_release.wheels.url_exists", lambda *a, **kw: True):
            # Succeeds
            url = find_ray_wheels_url(search_str)
            self.assertEqual(url, get_ray_wheels_url(repo, branch, commit, version))
