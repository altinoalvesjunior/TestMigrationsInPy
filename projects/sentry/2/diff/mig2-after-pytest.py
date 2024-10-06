from __future__ import absolute_import

import mock
import os
import pytest
import signal
import urllib

from django.conf import settings
from selenium import webdriver

def fin():
    # Teardown Selenium.
    browser.close()
    # TODO: remove this when fixed in: https://github.com/seleniumhq/selenium/issues/767
    browser.service.process.send_signal(signal.SIGTERM)
    browser.quit()
    request.addfinalizer(fin)
    return browser