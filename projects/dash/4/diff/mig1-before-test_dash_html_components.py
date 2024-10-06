import unittest
import dash_html_components

class TestDashHtmlComponents(unittest.TestCase):
    def test_imports(self):
        with open('./scripts/data/elements.txt') as f:
            elements = [
                s[0].upper() + s[1:] for s in
                f.read().split('\n')
            ]
            elements += ['MapEl', 'ObjectEl']
            for s in ['Map', 'Object']:
                elements.remove(s)
        print(dir(dash_html_components))
        self.assertEqual(
            set([d for d in dir(dash_html_components) if d[0] != '_' and d[0] == d[0].capitalize()]),
            set(elements)
        )