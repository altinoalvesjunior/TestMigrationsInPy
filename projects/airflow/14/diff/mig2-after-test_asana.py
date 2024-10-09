from __future__ import annotations

import os
from unittest.mock import patch

import pytest
from asana import Client
from pytest import param

from airflow.models import Connection
from airflow.providers.asana.hooks.asana import AsanaHook
from tests.test_utils.providers import get_provider_min_airflow_version, object_exists


class TestAsanaHook:
    def test_missing_password_raises(self):
        """
        Test that the Asana hook raises an exception if password not provided in connection.
        :return: None
        """
        with patch.object(AsanaHook, "get_connection", return_value=Connection(conn_type="asana")):
            hook = AsanaHook()
        with pytest.raises(ValueError):
            hook.get_conn()
