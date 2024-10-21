import importlib.util
import multiprocessing as mp
import os
import socket
import sys
import tempfile
import threading
import time
import unittest
from contextlib import contextmanager

import pytest

class BPDPlaybackTest(BPDTestHelper):
        def test_cmd_replay_gain(self):
            with self.run_bpd() as client:
                responses = client.send_commands(
                    ("replay_gain_mode", "track"),
                    ("replay_gain_status",),
                    ("replay_gain_mode", "notanoption"),
                )
            self._assert_failed(responses, bpd.ERROR_ARG, pos=2)
            assert "track" == responses[1].data["replay_gain_mode"]