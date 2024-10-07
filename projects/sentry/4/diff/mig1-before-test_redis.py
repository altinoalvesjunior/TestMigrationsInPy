from django.utils.encoding import force_text
from freezegun import freeze_time

from sentry.buffer.redis import RedisBuffer
from sentry.models import Group, Project
from sentry.testutils import TestCase
from sentry.utils import json


class RedisBufferTest(TestCase):
    def setUp(self):
        self.buf = RedisBuffer()