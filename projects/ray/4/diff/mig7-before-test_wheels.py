import os
import sys
import time
import unittest
from unittest.mock import patch

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