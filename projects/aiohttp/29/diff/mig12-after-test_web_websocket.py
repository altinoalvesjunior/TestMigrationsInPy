def test_closed_after_ctor():
    ws = WebSocketResponse()
    assert not ws.closed
    assert ws.close_code is None