import os
import unittest
from aiohttp import web

class StaticFileMixin(unittest.TestCase):

    def test_static_route_path_existence_check(self):
        directory = os.path.dirname(__file__)
        web.StaticResource("/", directory)
        nodirectory = os.path.join(directory, "nonexistent-uPNiOEAg5d")
        with self.assertRaises(ValueError):
            web.StaticResource("/", nodirectory)