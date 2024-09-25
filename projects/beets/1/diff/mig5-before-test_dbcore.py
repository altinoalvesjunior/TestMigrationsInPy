import os
import shutil
import sqlite3
import unittest
from tempfile import mkstemp

from beets import dbcore
from beets.test import _common