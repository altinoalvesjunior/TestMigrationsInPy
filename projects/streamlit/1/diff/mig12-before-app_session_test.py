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
    
    def test_disconnect_file_watchers_removes_refs(self):
        """Test that calling disconnect_file_watchers on the AppSession
        removes references to it so it is eligible to be garbage collected after the
        method is called.
        """
        session = _create_test_session()

        # Various listeners should have references to session file/pages/secrets changed
        # handlers.
        self.assertGreater(len(gc.get_referrers(session)), 0)

        session.disconnect_file_watchers()

        # Run the gc to ensure that we don't count refs to session from an object that
        # would have been garbage collected along with the session. We run the gc a few
        # times for good measure as otherwise we've previously seen weirdness in CI
        # where this test would fail for certain Python versions (exact reasons
        # unknown), so it seems like the first gc sweep may not always pick up the
        # session.
        gc.collect(2)
        gc.collect(2)
        gc.collect(2)

        self.assertEqual(len(gc.get_referrers(session)), 0)

        
    