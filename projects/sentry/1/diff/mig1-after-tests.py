import datetime
import mock
import pytest

from django.utils import timezone
from sentry.interfaces import Interface
from sentry.models import Event, Group, Project, MessageCountByMinute, ProjectCountByMinute, \
  SearchDocument
from sentry.utils.db import has_trending  # NOQA
from sentry.testutils import TestCase

@pytest.mark.skipif('not has_trending()')
class TrendsTest(TestCase):
    ...