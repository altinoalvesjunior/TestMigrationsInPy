import unittest
import gc
from unittest import mock
from aiohttp.client import ClientSession

class TestClientSession(unittest.TestCase):

    def test_del(self):
        conn = self.make_open_connector()
        session = ClientSession(loop=self.loop, connector=conn)
        self.loop.set_exception_handler(lambda loop, ctx: None)

        with self.assertWarns(ResourceWarning):
            del session
            gc.collect()