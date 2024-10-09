import logging
import unittest

from airflow.config_templates.airflow_local_settings import DEFAULT_LOGGING_CONFIG
from airflow.models import DAG, TaskInstance
from airflow.operators.dummy import DummyOperator
from airflow.utils.log.logging_mixin import set_context
from airflow.utils.state import DagRunState
from airflow.utils.timezone import datetime
from airflow.utils.types import DagRunType
from tests.test_utils.config import conf_vars
from tests.test_utils.db import clear_db_runs

DEFAULT_DATE = datetime(2019, 1, 1)
TASK_LOGGER = 'airflow.task'
TASK_HANDLER = 'task'
TASK_HANDLER_CLASS = 'airflow.utils.log.task_handler_with_custom_formatter.TaskHandlerWithCustomFormatter'
PREV_TASK_HANDLER = DEFAULT_LOGGING_CONFIG['handlers']['task']


class TestTaskHandlerWithCustomFormatter(unittest.TestCase):
    def setUp(self):
        DEFAULT_LOGGING_CONFIG['handlers']['task'] = {
            'class': TASK_HANDLER_CLASS,
            'formatter': 'airflow',
            'stream': 'sys.stdout',
        }
        logging.config.dictConfig(DEFAULT_LOGGING_CONFIG)
        logging.root.disabled = False
    def tearDown(self):
        clear_db_runs()
        DEFAULT_LOGGING_CONFIG['handlers']['task'] = PREV_TASK_HANDLER