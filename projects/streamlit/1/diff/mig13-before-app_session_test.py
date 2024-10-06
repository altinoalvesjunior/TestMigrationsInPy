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
        "streamlit.runtime.app_session.config.get_options_for_section",
        MagicMock(side_effect=_mock_get_options_for_section()),
    )
    @patch(
        "streamlit.runtime.app_session.source_util.get_pages",
        MagicMock(
            return_value={
                "hash1": {"page_name": "page1", "icon": "", "script_path": "script1"},
                "hash2": {"page_name": "page2", "icon": "🎉", "script_path": "script2"},
            }
        ),
    )
    @patch(
        "streamlit.runtime.app_session._generate_scriptrun_id",
        MagicMock(return_value="mock_scriptrun_id"),
    )
    async def test_enqueue_new_session_message(self):
        """The SCRIPT_STARTED event should enqueue a 'new_session' message."""
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
        )

        # Yield to let the AppSession's callbacks run.
        await asyncio.sleep(0)

        sent_messages = session._browser_queue._queue
        self.assertEqual(2, len(sent_messages))  # NewApp and SessionState messages
        session._clear_queue.assert_called_once()

        # Note that we're purposefully not very thoroughly testing new_session
        # fields below to avoid getting to the point where we're just
        # duplicating code in tests.
        new_session_msg = sent_messages[0].new_session
        self.assertEqual("mock_scriptrun_id", new_session_msg.script_run_id)

        self.assertTrue(new_session_msg.HasField("config"))
        self.assertEqual(
            config.get_option("server.allowRunOnSave"),
            new_session_msg.config.allow_run_on_save,
        )

        self.assertTrue(new_session_msg.HasField("custom_theme"))
        self.assertEqual("black", new_session_msg.custom_theme.text_color)

        init_msg = new_session_msg.initialize
        self.assertTrue(init_msg.HasField("user_info"))

        self.assertEqual(
            list(new_session_msg.app_pages),
            [
                AppPage(page_script_hash="hash1", page_name="page1", icon=""),
                AppPage(page_script_hash="hash2", page_name="page2", icon="🎉"),
            ],
        )

        add_script_run_ctx(ctx=orig_ctx)