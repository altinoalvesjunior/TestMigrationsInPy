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
    def test_check_db_fails(self):
            with self.assertRaisesRegex(ValueError, "no database"):
                dbcore.Model()._check_db()
            with self.assertRaisesRegex(ValueError, "no id"):
                ModelFixture1(self.db)._check_db()

            dbcore.Model(self.db)._check_db(need_id=False)