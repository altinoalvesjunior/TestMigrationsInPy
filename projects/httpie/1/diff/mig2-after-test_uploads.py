import os
from unittest import TestCase

import pytest

from httpie.input import ParseError
from tests import TestEnvironment, http, httpbin, HTTP_OK
from tests.fixtures import FILE_PATH_ARG, FILE_PATH, FILE_CONTENT


class MultipartFormDataFileUploadTest(TestCase):
    def test_non_existent_file_raises_parse_error(self):
        with pytest.raises(ParseError):
            http('--form', 'POST', httpbin('/post'), 'foo@/__does_not_exist__')