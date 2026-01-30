from kai11.core.template import extract_placeholders, render_template


def test_placeholder_extract_and_render():
    text = "Hello {name}"
    assert extract_placeholders(text) == {"name"}
    assert render_template(text, {"name": "Kai"}) == "Hello Kai"
