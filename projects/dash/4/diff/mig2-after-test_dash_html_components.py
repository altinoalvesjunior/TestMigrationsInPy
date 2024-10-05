import pytest
import dash_html_components as html

def test_sample_items():
    layout = html.Div(
        html.Div(html.Img(src="https://plotly.com/~chris/1638.png")),
        style={"color": "red"}
    )
    expected = (
        "Div(children=Div(Img(src='https://plotly.com/~chris/1638.png')), "
        "style={'color': 'red'})"
    )
    assert repr(layout) == expected
    assert layout._namespace == "dash_html_components"