import os
import shutil
import sqlite3
import unittest
from tempfile import mkstemp

from beets import dbcore
from beets.test import _common

class ModelFixture1(dbcore.Model):
    _table = "test"
    _flex_table = "testflex"
    _fields = {
        "id": dbcore.types.PRIMARY_ID,
        "field_one": dbcore.types.INTEGER,
        "field_two": dbcore.types.STRING,
    }
    _types = {
        "some_float_field": dbcore.types.FLOAT,
    }
    _sorts = {
        "some_sort": SortFixture,
    }
    _queries = {
        "some_query": QueryFixture,
    }

    @classmethod
    def _getters(cls):
        return {}

    def _template_funcs(self):
        return {}
    
class ModelTest(unittest.TestCase):
    def test_delete_non_existent_attribute(self):
        model = ModelFixture1()
        with pytest.raises(KeyError):
            del model["foo"]