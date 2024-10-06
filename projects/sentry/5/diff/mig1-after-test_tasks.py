from unittest.mock import patch
from urllib.parse import parse_qs
from uuid import uuid4

import pytest
import responses

from sentry.incidents.models import AlertRule, AlertRuleTriggerAction
from sentry.integrations.slack.utils import RedisRuleStatus
from sentry.models import Rule
from sentry.receivers.rules import DEFAULT_RULE_LABEL
from sentry.services.hybrid_cloud.integration.serial import serialize_integration
from sentry.tasks.integrations.slack import (
    find_channel_id_for_alert_rule,
    find_channel_id_for_rule,
    post_message,
)
from sentry.testutils.cases import TestCase
from sentry.testutils.helpers import install_slack
from sentry.testutils.silo import region_silo_test
from sentry.utils import json


@region_silo_test(stable=True)
class SlackTasksTest(TestCase):
    def setUp(self):
        self.integration = install_slack(self.organization)
        self.uuid = uuid4().hex

    @pytest.fixture(autouse=True)
    def setup_responses(self):
        responses.add(
            method=responses.POST,
            url="https://slack.com/api/chat.scheduleMessage",
            status=200,
            content_type="application/json",
            body=json.dumps(
                {"ok": "true", "channel": "chan-id", "scheduled_message_id": "Q1298393284"}
            ),
        )
        responses.add(
            method=responses.POST,
            url="https://slack.com/api/chat.deleteScheduledMessage",
            status=200,
            content_type="application/json",
            body=json.dumps({"ok": True}),
        )
        with responses.mock:
            yield