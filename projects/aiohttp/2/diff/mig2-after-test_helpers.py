import pytest
import unittest.mock


def test_parse_mimetype_1():
    assert helpers.parse_mimetype('') == ('', '', '', {})


def test_parse_mimetype_2():
    assert helpers.parse_mimetype('*') == ('*', '*', '', {})


def test_parse_mimetype_3():
    assert helpers.parse_mimetype(
        'application/json') == ('application', 'json', '', {})


def test_parse_mimetype_4():
    assert helpers.parse_mimetype(
        'application/json; charset=utf-8') == ('application', 'json', '', {'charset': 'utf-8'})


def test_parse_mimetype_5():
    assert helpers.parse_mimetype(
        '''application/json; charset=utf-8;''') == ('application', 'json', '', {'charset': 'utf-8'})


def test_parse_mimetype_6():
    assert helpers.parse_mimetype(
        'ApPlIcAtIoN/JSON;ChaRseT="UTF-8"') == ('application', 'json', '', {'charset': 'UTF-8'})


def test_parse_mimetype_7():
    assert helpers.parse_mimetype(
        'application/rss+xml') == ('application', 'rss', 'xml', {})


def test_parse_mimetype_8():
    assert helpers.parse_mimetype(
        'text/plain;base64') == ('text', 'plain', '', {'base64': ''})


class TestHelpers(unittest.TestCase):
    def test_parse_mimetype(self):
        self.assertEqual(helpers.parse_mimetype(''), ('', '', '', {}))
        self.assertEqual(helpers.parse_mimetype('*'), ('*', '*', '', {}))
        self.assertEqual(helpers.parse_mimetype(
            'application/json'), ('application', 'json', '', {}))
        self.assertEqual(helpers.parse_mimetype(
            'application/json; charset=utf-8'), ('application', 'json', '', {'charset': 'utf-8'}))
        self.assertEqual(helpers.parse_mimetype(
            '''application/json; charset=utf-8;'''), ('application', 'json', '', {'charset': 'utf-8'}))
        self.assertEqual(helpers.parse_mimetype(
            'ApPlIcAtIoN/JSON;ChaRseT="UTF-8"'), ('application', 'json', '', {'charset': 'UTF-8'}))
        self.assertEqual(helpers.parse_mimetype(
            'application/rss+xml'), ('application', 'rss', 'xml', {}))
        self.assertEqual(helpers.parse_mimetype(
            'text/plain;base64'), ('text', 'plain', '', {'base64': ''}))

    def test_basic_auth(self):
        # missing password here
        self.assertRaises(ValueError, helpers.BasicAuth, None)
        self.assertRaises(ValueError, helpers.BasicAuth, 'nkim', None)
        auth = helpers.BasicAuth('nkim')
        self.assertEqual(auth.login, 'nkim')
        self.assertEqual(auth.password, '')
        auth = helpers.BasicAuth('nkim', 'pwd')
        self.assertEqual(auth.login, 'nkim')
        self.assertEqual(auth.password, 'pwd')
        self.assertEqual(auth.encode(), 'Basic bmtpbTpwd2Q=')

    def test_invalid_formdata_params(self):
        with self.assertRaises(TypeError):
            helpers.FormData('asdasf')

    def test_invalid_formdata_params2(self):
        with self.assertRaises(TypeError):
            helpers.FormData('as')  # 2-char str is not allowed

    def test_invalid_formdata_content_type(self):
        form = helpers.FormData()
        invalid_vals = [0, 0.1, {}, [], b'foo']
        for invalid_val in invalid_vals:
            with self.assertRaises(TypeError):
                form.add_field('foo', 'bar', content_type=invalid_val)

    def test_invalid_formdata_filename(self):
        form = helpers.FormData()
        invalid_vals = [0, 0.1, {}, [], b'foo']
        for invalid_val in invalid_vals:
            with self.assertRaises(TypeError):
                form.add_field('foo', 'bar', filename=invalid_val)

    def test_invalid_formdata_content_transfer_encoding(self):
        form = helpers.FormData()
        invalid_vals = [0, 0.1, {}, [], b'foo']
        for invalid_val in invalid_vals:
            with self.assertRaises(TypeError):
                form.add_field(
                    'foo', 'bar', content_transfer_encoding=invalid_val)

    def test_reify(self):
        class A:
            @helpers.reify
            def prop(self):
                return 1

        a = A()
        self.assertEqual(1, a.prop)

    def test_reify_class(self):
        class A:
            @helpers.reify
            def prop(self):
                """Docstring."""
                return 1

        self.assertIsInstance(A.prop, helpers.reify)
        self.assertEqual('Docstring.', A.prop.__doc__)

    def test_reify_assignment(self):
        class A:
            @helpers.reify
            def prop(self):
                return 1

        a = A()
        with self.assertRaises(AttributeError):
            a.prop = 123


class TestAtoms(unittest.TestCase):
    def test_get_seconds_and_milliseconds(self):
        response = dict(status=200, output_length=1)
        request_time = 321.012345678901234
        atoms = helpers.atoms(None, None, response, None, request_time)
        self.assertEqual(atoms['T'], '321')
        self.assertEqual(atoms['D'], '012345')


class TestSafeAtoms(unittest.TestCase):
    def test_get_non_existing(self):
        atoms = helpers.SafeAtoms({}, MultiDict(), MultiDict())
        self.assertEqual(atoms['unknown'], '-')

    def test_get_lower(self):
        i_headers = MultiDict([('test', '123')])
        o_headers = MultiDict([('TEST', '123')])
        atoms = helpers.SafeAtoms({}, i_headers, o_headers)
        self.assertEqual(atoms['{test}i'], '123')
        self.assertEqual(atoms['{test}o'], '-')
        self.assertEqual(atoms['{TEST}o'], '123')
        self.assertEqual(atoms['{UNKNOWN}o'], '-')
        self.assertEqual(atoms['{UNKNOWN}'], '-')


class TestRequoting(unittest.TestCase):
    def test_requote_uri_with_unquoted_percents(self):
        # Ensure we handle unquoted percent signs in redirects.
        bad_uri = 'http://example.com/fiz?buz=%ppicture'
        quoted = 'http://example.com/fiz?buz=%25ppicture'
        self.assertEqual(quoted, helpers.requote_uri(bad_uri))

    def test_requote_uri_properly_requotes(self):
        # Ensure requoting doesn't break expectations.
        quoted = 'http://example.com/fiz?buz=%25ppicture'
        self.assertEqual(quoted, helpers.requote_uri(quoted))


def test_get_non_existing():
    atoms = helpers.SafeAtoms({}, MultiDict(), MultiDict())
    assert atoms['unknown'] == '-'


def test_get_lower():
    i_headers = MultiDict([('test', '123')])
    o_headers = MultiDict([('TEST', '123')])
    atoms = helpers.SafeAtoms({}, i_headers, o_headers)
    assert atoms['{test}i'] == '123'
    assert atoms['{test}o'] == '-'
    assert atoms['{TEST}o'] == '123'
    assert atoms['{UNKNOWN}o'] == '-'
    assert atoms['{UNKNOWN}'] == '-'


def test_requote_uri_with_unquoted_percents():
    # Ensure we handle unquoted percent signs in redirects.
    bad_uri = 'http://example.com/fiz?buz=%ppicture'
    quoted = 'http://example.com/fiz?buz=%25ppicture'
    assert quoted == helpers.requote_uri(bad_uri)


def test_requote_uri_properly_requotes():
    # Ensure requoting doesn't break expectations.
    quoted = 'http://example.com/fiz?buz=%25ppicture'
    assert quoted == helpers.requote_uri(quoted)
