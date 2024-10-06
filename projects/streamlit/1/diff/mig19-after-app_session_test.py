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

class PopulateCustomThemeMsgTest(unittest.TestCase):
    @patch("streamlit.runtime.app_session.config")
    def test_can_specify_some_options(self, patched_config):
        patched_config.get_options_for_section.side_effect = _mock_get_options_for_section(
            {
                # Leave base, primaryColor, and font defined.
                "backgroundColor": None,
                "secondaryBackgroundColor": None,
                "textColor": None,
            }
        )

        msg = ForwardMsg()
        new_session_msg = msg.new_session
        app_session._populate_theme_msg(new_session_msg.custom_theme)

        assert new_session_msg.HasField("custom_theme")
        assert new_session_msg.custom_theme.primary_color == "coral"
        # In proto3, primitive fields are technically always required and are
        # set to the type's zero value when undefined.
        assert new_session_msg.custom_theme.background_color == ""