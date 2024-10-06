import unittest
import dash_html_components

def test_sample_items(self):
        Div = dash_html_components.Div
        Img = dash_html_components.Img
        layout = Div(
            Div(
                Img(src='https://plotly.com/~chris/1638.png')
            ), style={'color': 'red'}
        )
        self.assertEqual(
            repr(layout),
            ''.join([
                "Div(children=Div(Img(src='https://plotly.com/~chris/1638.png')), "
                "style={'color': 'red'})"
            ])
        )
        self.assertEqual(
            layout._namespace, 'dash_html_components'
        )