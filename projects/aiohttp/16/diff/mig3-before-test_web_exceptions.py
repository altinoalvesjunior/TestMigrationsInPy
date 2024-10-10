import collections
import unittest
from aiohttp import web

class TestHTTPExceptions(unittest.TestCase):
    def test_terminal_classes_has_status_code(self):
        terminals = set()
        for name in dir(web):
            obj = getattr(web, name)
            if isinstance(obj, type) and issubclass(obj, web.HTTPException):
                terminals.add(obj)
        dup = frozenset(terminals)
        for cls1 in dup:
            for cls2 in dup:
                if cls1 in cls2.__bases__:
                    terminals.discard(cls1)
        for cls in terminals:
            self.assertIsNotNone(cls.status_code, cls)
        codes = collections.Counter(cls.status_code for cls in terminals)
        self.assertNotIn(None, codes)
        self.assertEqual(1, codes.most_common(1)[0][1])