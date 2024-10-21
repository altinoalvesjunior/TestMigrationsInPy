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
    def test_merge_project_parameters_override(self):
        """
        Tests that default workspace is successfully overridden
        :return:
        """
        conn = Connection(conn_type='asana', password='test', extra='{"extra__asana__workspace": "1"}')
        with patch.object(AsanaHook, "get_connection", return_value=conn):
            hook = AsanaHook()
        expected_merged_params = {"workspace": "2"}
        assert hook._merge_project_parameters({"workspace": "2"}) == expected_merged_params