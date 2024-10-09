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
    def test_merge_project_parameters_override(self):
        """
        Tests that default workspace is successfully overridden
        :return:
        """
        conn = Connection(conn_type='asana', password='test', extra='{"extra__asana__workspace": "1"}')
        with patch.object(AsanaHook, "get_connection", return_value=conn):
            hook = AsanaHook()
        expected_merged_params = {"workspace": "2"}
        self.assertEqual(
            expected_merged_params,
            hook._merge_project_parameters({"workspace": "2"}),
        )