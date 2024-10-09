import logging
import pytest

from airflow.config_templates.airflow_local_settings import DEFAULT_LOGGING_CONFIG
from airflow.models import DAG, DagRun, TaskInstance
from airflow.models.tasklog import LogTemplate
from airflow.operators.dummy import DummyOperator
from airflow.utils.log.logging_mixin import set_context
from airflow.utils.session import create_session
from airflow.utils.state import DagRunState
from airflow.utils.timezone import datetime
from airflow.utils.types import DagRunType
from tests.test_utils.config import conf_vars
from tests.test_utils.db import clear_db_runs

DEFAULT_DATE = datetime(2019, 1, 1)
TASK_HANDLER = 'task'
TASK_HANDLER_CLASS = 'airflow.utils.log.task_handler_with_custom_formatter.TaskHandlerWithCustomFormatter'
PREV_TASK_HANDLER = DEFAULT_LOGGING_CONFIG['handlers']['task']

DAG_ID = "task_handler_with_custom_formatter_dag"
TASK_ID = "task_handler_with_custom_formatter_task"


@pytest.fixture(scope="module", autouse=True)
def custom_task_log_handler_config():
    DEFAULT_LOGGING_CONFIG['handlers']['task'] = {
        'class': TASK_HANDLER_CLASS,
        'formatter': 'airflow',
        'stream': 'sys.stdout',
    }
    logging.config.dictConfig(DEFAULT_LOGGING_CONFIG)
    logging.root.disabled = False
    yield
    DEFAULT_LOGGING_CONFIG['handlers']['task'] = PREV_TASK_HANDLER
    logging.config.dictConfig(DEFAULT_LOGGING_CONFIG)