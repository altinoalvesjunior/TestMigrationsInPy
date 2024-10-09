from __future__ import annotations

import unittest
from unittest.mock import patch

from asana import Client

from airflow.models import Connection
from airflow.providers.asana.hooks.asana import AsanaHook


class TestAsanaHook(unittest.TestCase):
    """
    Tests for AsanaHook Asana client retrieval
    """
    def test_merge_find_task_parameters_specified_project_overrides_workspace(self):
        """
        Test that merge_find_task_parameters uses the method parameter project over the default workspace
        if it is available
        :return: None
        """
        conn = Connection(
            conn_type="asana",
            password="test",
            extra='{"extra__asana__workspace": "1"}',
        )
        with patch.object(AsanaHook, "get_connection", return_value=conn):
            hook = AsanaHook()
        expected_merged_params = {"project": "2"}
        self.assertEqual(
            expected_merged_params,
            hook._merge_find_task_parameters({"project": "2"}),
        )