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
    def test_cmd_mixrampdelay(self):
            with self.run_bpd() as client:
                responses = client.send_commands(
                    ("mixrampdelay", "2"),
                    ("status",),
                    ("mixrampdelay", "nan"),
                    ("status",),
                    ("mixrampdelay", "-2"),
                )
            self._assert_failed(responses, bpd.ERROR_ARG, pos=4)
            self.assertAlmostEqual(2, float(responses[1].data["mixrampdelay"]))
            assert "mixrampdelay" not in responses[3].data