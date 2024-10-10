    def request_from_message(self, message):
        self.app = mock.Mock()
        self.app._debug = False
        self.app.on_response_prepare = signals.Signal(self.app)
        self.payload = mock.Mock()
        self.transport = mock.Mock()
        self.reader = mock.Mock()
        self.writer = mock.Mock()
        req = Request(self.app, message, self.payload,
                      self.transport, self.reader, self.writer)
        return req

    @mock.patch('aiohttp.web_reqrep.ResponseImpl')
    def test_force_compression_no_accept_deflate(self, ResponseImpl):
        req = self.make_request('GET', '/')
        resp = StreamResponse()

        resp.enable_compression(ContentCoding.deflate)
        self.assertTrue(resp.compression)

        msg = self.loop.run_until_complete(resp.prepare(req))
        msg.add_compression_filter.assert_called_with('deflate')
        self.assertEqual('deflate', resp.headers.get(hdrs.CONTENT_ENCODING))