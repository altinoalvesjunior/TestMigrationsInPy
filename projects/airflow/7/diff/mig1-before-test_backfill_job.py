import datetime
import json
import logging
import threading
import unittest
from unittest.mock import patch

from parameterized import parameterized

from airflow.models import DAG, DagBag, Pool, TaskInstance as TI
from tests.test_utils.db import clear_db_pools, clear_db_runs, set_default_pool_slots


class TestBackfillJob(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dagbag = DagBag(include_examples=True)

    @staticmethod
    def clean_db():
        clear_db_runs()
        clear_db_pools()

    @staticmethod
    def clean_db():
        clear_db_runs()
        clear_db_pools()
        