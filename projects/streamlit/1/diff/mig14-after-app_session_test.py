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
    @patch(
        "streamlit.runtime.app_session._generate_scriptrun_id",
        MagicMock(return_value="mock_scriptrun_id"),
    )
    async def test_new_session_message_includes_fragment_ids(self):
        session = _create_test_session(asyncio.get_running_loop())

        orig_ctx = get_script_run_ctx()
        ctx = ScriptRunContext(
            session_id="TestSessionID",
            _enqueue=session._enqueue_forward_msg,
            query_string="",
            session_state=MagicMock(),
            uploaded_file_mgr=MagicMock(),
            main_script_path="",
            page_script_hash="",
            user_info={"email": "test@test.com"},
            fragment_storage=MemoryFragmentStorage(),
        )
        add_script_run_ctx(ctx=ctx)

        mock_scriptrunner = MagicMock(spec=ScriptRunner)
        session._scriptrunner = mock_scriptrunner
        session._clear_queue = MagicMock()

        # Send a mock SCRIPT_STARTED event.
        session._on_scriptrunner_event(
            sender=mock_scriptrunner,
            event=ScriptRunnerEvent.SCRIPT_STARTED,
            page_script_hash="",
            fragment_ids_this_run={"my_fragment_id"},
        )

        # Yield to let the AppSession's callbacks run.
        await asyncio.sleep(0)

        sent_messages = session._browser_queue._queue
        assert len(sent_messages) == 2  # NewApp and SessionState messages
        session._clear_queue.assert_not_called()

        new_session_msg = sent_messages[0].new_session
        assert new_session_msg.fragment_ids_this_run == ["my_fragment_id"]

        add_script_run_ctx(ctx=orig_ctx)