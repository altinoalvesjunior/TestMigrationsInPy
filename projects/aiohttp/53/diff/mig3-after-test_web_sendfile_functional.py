import os
import pytest
from aiohttp import web

def test_static_route_path_existence_check():
    directory = os.path.dirname(__file__)
    web.StaticResource("/", directory)
    nodirectory = os.path.join(directory, "nonexistent-uPNiOEAg5d")
    with pytest.raises(ValueError):
        web.StaticResource("/", nodirectory)