class AppSessionTest(unittest.TestCase):
    def test_unique_id(self):
        """Each AppSession should have a unique ID"""
        session1 = _create_test_session()
        session2 = _create_test_session()
        assert session1.id != session2.id