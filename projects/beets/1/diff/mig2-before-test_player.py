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

class BPDPlaybackTest(BPDTestHelper):
    def test_cmd_mixrampdb(self):
            with self.run_bpd() as client:
                responses = client.send_commands(("mixrampdb", "-17"), ("status",))
            self._assert_ok(*responses)
            self.assertAlmostEqual(-17, float(responses[1].data["mixrampdb"]))