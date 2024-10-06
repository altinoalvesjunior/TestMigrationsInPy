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

class AppSessionScriptEventTest(IsolatedAsyncioTestCase):
    """Tests for AppSession's ScriptRunner event handling."""
    
    async def test_event_handler_asserts_if_called_off_event_loop(self):
        """AppSession._handle_scriptrunner_event_on_event_loop will assert
        if it's called from another event loop (or no event loop).
        """
        event_loop = asyncio.get_running_loop()
        session = _create_test_session(event_loop)

        # Pretend we're calling this function from a thread with another event_loop.
        with patch(
            "streamlit.runtime.app_session.asyncio.get_running_loop",
            return_value=MagicMock(),
        ):
            with pytest.raises(AssertionError):
                session._handle_scriptrunner_event_on_event_loop(
                    sender=MagicMock(), event=ScriptRunnerEvent.SCRIPT_STARTED
                )
    