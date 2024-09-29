def test_creates_fragment_storage_on_init(self):
        session = _create_test_session()
        # NOTE: We only call assertIsNotNone here because protocols can't be used with
        # isinstance (there's no need to as the static type checker already ensures
        # the field has the correct type), and we don't want to mark
        # MemoryFragmentStorage as @runtime_checkable.
        self.assertIsNotNone(session._fragment_storage)

    def test_clear_cache_resets_session_state(self):
        session = _create_test_session()
        session._session_state["foo"] = "bar"
        session._handle_clear_cache_request()
        self.assertTrue("foo" not in session._session_state)
