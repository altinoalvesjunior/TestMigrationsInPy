from django.utils.encoding import force_text
from freezegun import freeze_time

from sentry import options
from sentry.buffer.redis import RedisBuffer
from sentry.models import Group, Project
from sentry.utils import json


class TestRedisBuffer:
    @pytest.fixture(autouse=True)
    def setup_buffer(self, buffer):
        self.buf = buffer
