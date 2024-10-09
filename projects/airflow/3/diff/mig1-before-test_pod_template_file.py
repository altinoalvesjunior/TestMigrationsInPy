import re
import unittest
from os import remove
from os.path import dirname, realpath
from shutil import copyfile

import jmespath
from parameterized import parameterized

from tests.helm_template_generator import render_chart

ROOT_FOLDER = realpath(dirname(realpath(__file__)) + "/..")

class PodTemplateFileTest(unittest.TestCase):
    def setUp(self):
        copyfile(
            ROOT_FOLDER + "/files/pod-template-file.kubernetes-helm-yaml",
            ROOT_FOLDER + "/templates/pod-template-file.yaml",
        )
    def tearDown(self):
        remove(ROOT_FOLDER + "/templates/pod-template-file.yaml")
