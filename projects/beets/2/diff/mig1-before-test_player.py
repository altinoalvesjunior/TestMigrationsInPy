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

# Mock GstPlayer so that the forked process doesn't attempt to import gi:
from unittest import mock

import confuse
import yaml

from beets.test.helper import PluginTestCase
from beets.util import bluelet
from beetsplug import bpd

gstplayer = importlib.util.module_from_spec(
    importlib.util.find_spec("beetsplug.bpd.gstplayer")
)

class MPCClient:
        def __init__(self, sock, do_hello=True):
        self.sock = sock
        self.buf = b""
        if do_hello:
            hello = self.get_response()
            if not hello.ok:
                raise RuntimeError("Bad hello")

    def get_response(self, force_multi=None):
        """Wait for a full server response and wrap it in a helper class.
        If the request was a batch request then this will return a list of
        `MPCResponse`s, one for each processed subcommand.
        """

        response = b""
        responses = []
        while True:
            line = self.readline()
            response += line
            if line.startswith(b"OK") or line.startswith(b"ACK"):
                if force_multi or any(responses):
                    if line.startswith(b"ACK"):
                        responses.append(MPCResponse(response))
                        n_remaining = force_multi - len(responses)
                        responses.extend([None] * n_remaining)
                    return responses
                else:
                    return MPCResponse(response)
            if line.startswith(b"list_OK"):
                responses.append(MPCResponse(response))
                response = b""
            elif not line:
                raise RuntimeError(f"Unexpected response: {line!r}")

    def serialise_command(self, command, *args):
        cmd = [command.encode("utf-8")]
        for arg in [a.encode("utf-8") for a in args]:
            if b" " in arg:
                cmd.append(b'"' + arg + b'"')
            else:
                cmd.append(arg)
        return b" ".join(cmd) + b"\n"

    def send_command(self, command, *args):
        request = self.serialise_command(command, *args)
        self.sock.sendall(request)
        return self.get_response()

    def send_commands(self, *commands):
        """Use MPD command batching to send multiple commands at once.
        Each item of commands is a tuple containing a command followed by
        any arguments.
        """

        requests = []
        for command_and_args in commands:
            command = command_and_args[0]
            args = command_and_args[1:]
            requests.append(self.serialise_command(command, *args))
        requests.insert(0, b"command_list_ok_begin\n")
        requests.append(b"command_list_end\n")
        request = b"".join(requests)
        self.sock.sendall(request)
        return self.get_response(force_multi=len(commands))

class BPDTestHelper(PluginTestCase):
    db_on_disk = True
    plugin = "bpd"

    def setUp(self):
        super().setUp()
        self.item1 = self.add_item(
            title="Track One Title",
            track=1,
            album="Album Title",
            artist="Artist Name",
        )
        self.item2 = self.add_item(
            title="Track Two Title",
            track=2,
            album="Album Title",
            artist="Artist Name",
        )
        self.lib.add_album([self.item1, self.item2])

    @contextmanager
    def run_bpd(
        self,
        host="localhost",
        password=None,
        do_hello=True,
        second_client=False,
    ):
        """Runs BPD in another process, configured with the same library
        database as we created in the setUp method. Exposes a client that is
        connected to the server, and kills the server at the end.
        """
        # Create a config file:
        config = {
            "pluginpath": [os.fsdecode(self.temp_dir)],
            "plugins": "bpd",
            # use port 0 to let the OS choose a free port
            "bpd": {"host": host, "port": 0, "control_port": 0},
        }
        if password:
            config["bpd"]["password"] = password
        config_file = tempfile.NamedTemporaryFile(
            mode="wb",
            dir=os.fsdecode(self.temp_dir),
            suffix=".yaml",
            delete=False,
        )
        config_file.write(
            yaml.dump(config, Dumper=confuse.Dumper, encoding="utf-8")
        )
        config_file.close()

        # Fork and launch BPD in the new process:
        assigned_port = mp.Queue(2)  # 2 slots, `control_port` and `port`
        server = mp.Process(
            target=start_server,
            args=(
                [
                    "--library",
                    self.config["library"].as_filename(),
                    "--directory",
                    os.fsdecode(self.libdir),
                    "--config",
                    os.fsdecode(config_file.name),
                    "bpd",
                ],
                assigned_port,
            ),
        )
        server.start()

        try:
            assigned_port.get(timeout=1)  # skip control_port
            port = assigned_port.get(timeout=0.5)  # read port

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.connect((host, port))

                if second_client:
                    sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    try:
                        sock2.connect((host, port))
                        yield (
                            MPCClient(sock, do_hello),
                            MPCClient(sock2, do_hello),
                        )
                    finally:
                        sock2.close()

                else:
                    yield MPCClient(sock, do_hello)
            finally:
                sock.close()
        finally:
            server.terminate()
            server.join(timeout=0.2)

class BPDPlaybackTest(BPDTestHelper):
    test_implements_playback = implements(
        {
            "random",
        }
    )

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