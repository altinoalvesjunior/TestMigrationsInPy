from __future__ import annotations

import pytest
from flask_appbuilder import SQLA

from airflow import settings
from airflow.security import permissions
from airflow.www import app as application
from tests.test_utils.api_connexion_utils import create_user, delete_role
from tests.test_utils.www import check_content_in_response, check_content_not_in_response, client_with_login

PERMISSIONS_TESTS_PARAMS = [
    (
        "/resetpassword/form?pk={user.id}",
        (permissions.ACTION_CAN_READ, permissions.RESOURCE_PASSWORD),
        "Reset Password Form",
    ),
    (
        "/resetmypassword/form",
        (permissions.ACTION_CAN_READ, permissions.RESOURCE_MY_PASSWORD),
        "Reset Password Form",
    ),
    (
        "/users/userinfo/",
        (permissions.ACTION_CAN_READ, permissions.RESOURCE_MY_PROFILE),
        "Your user information",
    ),
    ("/userinfoeditview/form", (permissions.ACTION_CAN_EDIT, permissions.RESOURCE_MY_PROFILE), "Edit User"),
    ("/users/add", (permissions.ACTION_CAN_CREATE, permissions.RESOURCE_USER), "Add User"),
    ("/users/list/", (permissions.ACTION_CAN_READ, permissions.RESOURCE_USER), "List Users"),
    ("/users/show/{user.id}", (permissions.ACTION_CAN_READ, permissions.RESOURCE_USER), "Show User"),
    ("/users/edit/{user.id}", (permissions.ACTION_CAN_EDIT, permissions.RESOURCE_USER), "Edit User"),
]

class TestSecurity:
    @pytest.mark.parametrize("url, _, expected_text", PERMISSIONS_TESTS_PARAMS)
    def test_user_model_view_with_access(self, url, expected_text, _):
        user_without_access = create_user(
            self.app,
            username="no_access",
            role_name="role_no_access",
            permissions=[
                (permissions.ACTION_CAN_READ, permissions.RESOURCE_WEBSITE),
            ],
        )
        client = client_with_login(
            self.app,
            username="no_access",
            password="no_access",
        )
        response = client.get(url.replace("{user.id}", str(user_without_access.id)), follow_redirects=True)
        check_content_not_in_response(expected_text, response)
