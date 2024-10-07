from __future__ import unicode_literals
import pytest

from cookiecutter import generate

@pytest.mark.usefixtures("clean_system")
def test_generate_context_with_default():
    context = generate.generate_context(
        context_file='tests/test-generate-context/test.json',
        default_context={"1": 3}
    )
    assert context == {"test": {"1": 3, "some_key": "some_val"}}