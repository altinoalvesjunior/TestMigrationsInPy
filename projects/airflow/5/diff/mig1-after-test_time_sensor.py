from __future__ import annotations

from datetime import datetime, time
from unittest.mock import patch

import freezegun
import pendulum
import pytest

from airflow.exceptions import TaskDeferred
from airflow.models.dag import DAG
from airflow.sensors.time_sensor import TimeSensor, TimeSensorAsync
from airflow.triggers.temporal import DateTimeTrigger
from airflow.utils import timezone

DEFAULT_TIMEZONE = "Asia/Singapore"  # UTC+08:00
DEFAULT_DATE_WO_TZ = datetime(2015, 1, 1)
DEFAULT_DATE_WITH_TZ = datetime(2015, 1, 1, tzinfo=pendulum.tz.timezone(DEFAULT_TIMEZONE))


@patch(
    "airflow.sensors.time_sensor.timezone.utcnow",
    return_value=timezone.datetime(2020, 1, 1, 23, 0).replace(tzinfo=timezone.utc),
)
class TestTimeSensor:
    @pytest.mark.parametrize(
        "default_timezone, start_date, expected",
        [
            ("UTC", DEFAULT_DATE_WO_TZ, True),
            ("UTC", DEFAULT_DATE_WITH_TZ, False),
            (DEFAULT_TIMEZONE, DEFAULT_DATE_WO_TZ, False),
        ],
    )
    def test_timezone(self, mock_utcnow, default_timezone, start_date, expected):
        with patch("airflow.settings.TIMEZONE", pendulum.timezone(default_timezone)):
            dag = DAG("test", default_args={"start_date": start_date})
            op = TimeSensor(task_id="test", target_time=time(10, 0), dag=dag)
            assert op.poke(None) == expected