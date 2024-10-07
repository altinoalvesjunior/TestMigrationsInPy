from __future__ import unicode_literals
import pytest

from cookiecutter import generate

@pytest.mark.usefixtures("clean_system")
def test_generate_context_with_extra():
    """ Call `generate_context()` with extra_context. """
    context = generate.generate_context(
        context_file='tests/test-generate-context/test.json',
        extra_context={'1': 4},
    )
    assert context == {'test': {'1': 4, 'some_key': 'some_val'}}