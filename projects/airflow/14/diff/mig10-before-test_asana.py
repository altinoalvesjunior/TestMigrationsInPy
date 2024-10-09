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
    def test_merge_find_task_parameters_default_workspace(self):
        """
        Test that merge_find_task_parameters correctly merges the default and method parameters when we
        do not override the default workspace.
        :return: None
        """
        conn = Connection(conn_type="asana", password="test", extra='{"extra__asana__workspace": "1"}')
        with patch.object(AsanaHook, "get_connection", return_value=conn):
            hook = AsanaHook()
        expected_merged_params = {"workspace": "1", "assignee": "1"}
        self.assertEqual(
            expected_merged_params,
            hook._merge_find_task_parameters({"assignee": "1"}),
        )