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
    def test_merge_find_task_parameters_default_project(self):
        """
        Test that merge_find_task_parameters correctly merges the default and method parameters when we
        do not override the default project.
        :return: None
        """
        conn = Connection(conn_type="asana", password="test", extra='{"extra__asana__project": "1"}')
        with patch.object(AsanaHook, "get_connection", return_value=conn):
            hook = AsanaHook()
        expected_merged_params = {"project": "1"}
        assert hook._merge_find_task_parameters({}) == expected_merged_params