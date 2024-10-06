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
    
    @patch("streamlit.runtime.app_session.AppSession._enqueue_forward_msg", MagicMock())
    def test_sets_state_to_not_running_on_rerun_event(self):
        session = _create_test_session()
        session._create_scriptrunner(initial_rerun_data=RerunData())
        session._state = AppSessionState.APP_IS_RUNNING

        with patch(
            "streamlit.runtime.app_session.asyncio.get_running_loop",
            return_value=session._event_loop,
        ):
            session._handle_scriptrunner_event_on_event_loop(
                sender=session._scriptrunner,
                event=ScriptRunnerEvent.SCRIPT_STOPPED_FOR_RERUN,
                forward_msg=ForwardMsg(),
            )

            assert session._state == AppSessionState.APP_NOT_RUNNING
    