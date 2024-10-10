from aiohttp import web

def test_all_http_exceptions_exported():
    assert 'HTTPException' in web.__all__
    for name in dir(web):
        if name.startswith('_'):
            continue
        obj = getattr(web, name)
        if isinstance(obj, type) and issubclass(obj, web.HTTPException):
            assert name in web.__all__