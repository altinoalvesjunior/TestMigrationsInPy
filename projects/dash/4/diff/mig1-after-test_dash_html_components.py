import pytest
import dash_html_components as html

def test_imports():
    with open("./scripts/data/elements.txt") as f:
        elements = [s[0].upper() + s[1:] for s in f.read().split("\n")]
        elements += ["MapEl", "ObjectEl"]
        for s in ["Map", "Object"]:
            elements.remove(s)
    dir_set = set(
        [
            d
            for d in dir(html)
            if d[0] != "_" and d[0] == d[0].capitalize()
        ]
    )
    assert dir_set == set(elements)