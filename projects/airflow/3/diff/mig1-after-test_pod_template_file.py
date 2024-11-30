import re
import sys
import unittest
from shutil import copyfile, copytree
from tempfile import TemporaryDirectory

import pytest

class PodTemplateFileTest(unittest.TestCase):
    @classmethod
    @pytest.fixture(autouse=True, scope="class")
    def isolate_chart(cls):
        with TemporaryDirectory() as tmp_dir:
            cls.temp_chart_dir = tmp_dir + "/chart"
            copytree(sys.path[0], cls.temp_chart_dir)
            copyfile(
                cls.temp_chart_dir + "/files/pod-template-file.kubernetes-helm-yaml",
                cls.temp_chart_dir + "/templates/pod-template-file.yaml",
            )
            yield