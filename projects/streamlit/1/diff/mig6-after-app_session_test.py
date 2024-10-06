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

class AppSessionTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        mock_runtime = MagicMock(spec=Runtime)
        mock_runtime.media_file_mgr = MediaFileManager(
            MemoryMediaFileStorage("/mock/media")
        )
        mock_runtime.cache_storage_manager = MemoryCacheStorageManager()
        Runtime._instance = mock_runtime

    def tearDown(self) -> None:
        super().tearDown()
        Runtime._instance = None
    
    @patch("streamlit.runtime.app_session.ScriptRunner")
    def test_create_scriptrunner(self, mock_scriptrunner: MagicMock):
        """Test that _create_scriptrunner does what it should."""
        session = _create_test_session()
        assert session._scriptrunner is None

        session._create_scriptrunner(initial_rerun_data=RerunData())

        # Assert that the ScriptRunner constructor was called.
        mock_scriptrunner.assert_called_once_with(
            session_id=session.id,
            main_script_path=session._script_data.main_script_path,
            session_state=session._session_state,
            uploaded_file_mgr=session._uploaded_file_mgr,
            script_cache=session._script_cache,
            initial_rerun_data=RerunData(),
            user_info={"email": "test@test.com"},
            fragment_storage=session._fragment_storage,
        )

        assert session._scriptrunner is not None

        # And that the ScriptRunner was initialized and started.
        scriptrunner: MagicMock = cast(MagicMock, session._scriptrunner)
        scriptrunner.on_event.connect.assert_called_once_with(
            session._on_scriptrunner_event
        )
        scriptrunner.start.assert_called_once()
    
    