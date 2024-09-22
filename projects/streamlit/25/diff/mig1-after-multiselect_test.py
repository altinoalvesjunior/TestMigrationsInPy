def test_get_default_count(self, default, expected_count):
        assert _get_default_count(default) == expected_count