import collections
from aiohttp import web

def test_terminal_classes_has_status_code():
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
        assert cls.status_code is not None
    codes = collections.Counter(cls.status_code for cls in terminals)
    assert None not in codes
    assert 1 == codes.most_common(1)[0][1]