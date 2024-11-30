import datetime
import json
import logging
import threading
from unittest.mock import patch

import pytest

from airflow.models import DAG, DagBag, Pool, TaskInstance as TI
from tests.test_utils.db import clear_db_pools, clear_db_runs, set_default_pool_slots

@pytest.fixture(scope="module")
def dag_bag():
    return DagBag(include_examples=True)

class TestBackfillJob:
    @classmethod
    def setUpClass(cls):
        cls.dagbag = DagBag(include_examples=True)
        
    @staticmethod
    def clean_db():
        clear_db_runs()
        clear_db_pools()