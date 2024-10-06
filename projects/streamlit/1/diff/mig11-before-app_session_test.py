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
    
    @patch(
        "streamlit.runtime.app_session.secrets_singleton.file_change_listener.disconnect"
    )
    def test_disconnect_file_watchers(self, patched_secrets_disconnect):
        session = _create_test_session()

        with patch.object(
            session._local_sources_watcher, "close"
        ) as patched_close_local_sources_watcher, patch.object(
            session, "_stop_config_listener"
        ) as patched_stop_config_listener, patch.object(
            session, "_stop_pages_listener"
        ) as patched_stop_pages_listener:
            session.disconnect_file_watchers()

            patched_close_local_sources_watcher.assert_called_once()
            patched_stop_config_listener.assert_called_once()
            patched_stop_pages_listener.assert_called_once()
            patched_secrets_disconnect.assert_called_once_with(
                session._on_secrets_file_changed
            )

            self.assertIsNone(session._local_sources_watcher)
            self.assertIsNone(session._stop_config_listener)
            self.assertIsNone(session._stop_pages_listener)
        
    