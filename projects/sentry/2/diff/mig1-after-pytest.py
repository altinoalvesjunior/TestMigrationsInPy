from __future__ import absolute_import

import mock
import os
import pytest
import signal
import urllib

from django.conf import settings
from selenium import webdriver

@pytest.fixture(scope='session')
def percy(request, browser):
    import percy
    # Initialize Percy.
    loader = percy.ResourceLoader(
        root_dir=settings.STATIC_ROOT,
        base_url=urllib.quote(settings.STATIC_URL),
        webdriver=browser,
    )
    percy_config = percy.Config(default_widths=settings.PERCY_DEFAULT_TESTING_WIDTHS)
    percy = percy.Runner(loader=loader, config=percy_config)
    percy.initialize_build()
    request.addfinalizer(percy.finalize_build)
    return percy

@pytest.fixture(scope='session')
def browser(request):
    # Initialize Selenium.
    # NOTE: this relies on the phantomjs binary packaged from npm to be in the right
    # location in node_modules.
    phantomjs_path = os.path.join(
        settings.NODE_MODULES_ROOT,
        'phantomjs-prebuilt',
        'bin',
        'phantomjs',
    )
    browser = webdriver.PhantomJS(executable_path=phantomjs_path)