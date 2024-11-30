from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible.module_utils.network.common.utils import conditional, Template

def test_template():
    tmpl = Template()
    assert 'foo' == tmpl('{{ test }}', {'test': 'foo'})