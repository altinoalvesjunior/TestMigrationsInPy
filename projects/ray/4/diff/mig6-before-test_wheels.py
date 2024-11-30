import os
import sys
import time
import unittest
from unittest.mock import patch

class WheelsFinderTest(unittest.TestCase):
    def setUp(self) -> None:
        for key in os.environ:
            if key.startswith("BUILDKITE"):
                os.environ.pop(key)