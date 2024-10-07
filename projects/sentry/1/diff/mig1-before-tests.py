import datetime
import mock

from django.utils import timezone
from nose.plugins.skip import SkipTest
from sentry.interfaces import Interface
from sentry.models import Event, Group, Project, MessageCountByMinute, ProjectCountByMinute, \
  SearchDocument
from sentry.utils.db import has_trending
from sentry.testutils import TestCase

class TrendsTest(TestCase):
    def setUp(self):
        if not has_trending():
            raise SkipTest('This database does not support trends.')