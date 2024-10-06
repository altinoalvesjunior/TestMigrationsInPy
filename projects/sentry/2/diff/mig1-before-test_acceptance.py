import signal
import urllib
import os
import percy
from django.conf import settings
from selenium import webdriver
from sentry.testutils import LiveServerTestCase

class AcceptanceTest(LiveServerTestCase):
    # Use class setup/teardown to hold Selenium and Percy state across all acceptance tests.
    # For Selenium, this is done for performance to re-use the same browser across tests.
    # For Percy, this is done to call initialize and then finalize at the very end after all tests.
    #
    # TODO: if acceptance tests are split across files, this will need to be refactored into a
    # pytest plugin/fixture or something else that can manage global state.
    @classmethod
    def setUpClass(cls):
        super(AcceptanceTest, cls).setUpClass()
        # Initialize Selenium.
        # NOTE: this relies on the phantomjs binary packaged from npm to be in the right
        # location in node_modules.
        phantomjs_path = os.path.join(
            settings.NODE_MODULES_ROOT,
            'phantomjs-prebuilt',
            'bin',
            'phantomjs',
        )
        cls.browser = webdriver.PhantomJS(executable_path=phantomjs_path)
        # Initialize Percy.
        loader = percy.ResourceLoader(
            root_dir=settings.STATIC_ROOT,
            base_url=urllib.quote(settings.STATIC_URL),
            webdriver=cls.browser,
        )
        percy_config = percy.Config(default_widths=settings.PERCY_DEFAULT_TESTING_WIDTHS)
        cls.percy = percy.Runner(loader=loader, config=percy_config)
        cls.percy.initialize_build()