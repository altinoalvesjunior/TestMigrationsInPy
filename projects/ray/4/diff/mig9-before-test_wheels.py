import os
import sys
import time
import unittest
from unittest.mock import patch

class WheelsFinderTest(unittest.TestCase):
    @patch("ray_release.wheels.get_ray_version", lambda *a, **kw: "3.0.0.dev0")
    def testFindRayWheelsBuildkite(self):
        repo = DEFAULT_REPO
        branch = "master"
        commit = "1234" * 10
        version = "3.0.0.dev0"

        os.environ["BUILDKITE_COMMIT"] = commit

        url = find_ray_wheels_url()

        self.assertEqual(url, get_ray_wheels_url(repo, branch, commit, version))

        branch = "branched"
        os.environ["BUILDKITE_BRANCH"] = branch

        url = find_ray_wheels_url()

        self.assertEqual(url, get_ray_wheels_url(repo, branch, commit, version))
