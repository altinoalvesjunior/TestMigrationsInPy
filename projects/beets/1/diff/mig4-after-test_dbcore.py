import os
import shutil
import sqlite3
import unittest
from tempfile import mkstemp

import pytest
from beets import dbcore
from beets.test import _common