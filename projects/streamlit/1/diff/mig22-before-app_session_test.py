import asyncio
import gc
import threading
import unittest
from asyncio import AbstractEventLoop
from typing import Any, Callable, List, Optional, cast
from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch

import pytest

import streamlit.runtime.app_session as app_session
from streamlit.runtime.app_session import AppSession, AppSessionState

from streamlit.runtime.uploaded_file_manager import (
    UploadedFileManager,
)

class ShouldRerunOnFileChangeTest(unittest.TestCase):
    def test_returns_true_if_changed_file_is_not_page(self):
        session = _create_test_session()
        session._client_state.page_script_hash = "hash1"

        self.assertEqual(
            session._should_rerun_on_file_change("some_other_file.py"), True
        )
