def test_creates_session_state_on_init(self):
        session = _create_test_session()
        assert isinstance(session.session_state, SessionState)