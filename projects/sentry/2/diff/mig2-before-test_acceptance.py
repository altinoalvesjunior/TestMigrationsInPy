import signal
import urllib
import os
import percy
from django.conf import settings
from selenium import webdriver
from sentry.testutils import LiveServerTestCase

class AcceptanceTest(LiveServerTestCase):
    @classmethod
    def tearDownClass(cls):
        # Teardown Selenium.
        cls.browser.close()
        # TODO: remove this when fixed in: https://github.com/seleniumhq/selenium/issues/767
        cls.browser.service.process.send_signal(signal.SIGTERM)
        cls.browser.quit()
        # Finalize Percy build.
        cls.percy.finalize_build()
        super(AcceptanceTest, cls).tearDownClass()