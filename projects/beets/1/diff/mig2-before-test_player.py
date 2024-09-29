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

from beetsplug import bpd

class BPDPlaybackTest(BPDTestHelper):
    def test_cmd_crossfade(self):
            with self.run_bpd() as client:
                responses = client.send_commands(
                    ("status",),
                    ("crossfade", "123"),
                    ("status",),
                    ("crossfade", "-2"),
                )
                response = client.send_command("crossfade", "0.5")
            self._assert_failed(responses, bpd.ERROR_ARG, pos=3)
            self._assert_failed(response, bpd.ERROR_ARG)
            assert "xfade" not in responses[0].data
            self.assertAlmostEqual(123, int(responses[2].data["xfade"]))