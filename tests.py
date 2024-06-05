# tests.py
import pytest
from app import parse_markdown

def test_bold_text():
    md_text = "This is **bold** text."
    expected_html = "<p>This is <b>bold</b> text.</p>"
    expected_ansi = "This is \033[1mbold\033[0m text."
    assert parse_markdown(md_text, 'HTML') == expected_html
    assert parse_markdown(md_text, 'ANSI') == expected_ansi

def test_italic_text():
    md_text = "This is _italic_ text."
    expected_html = "<p>This is <i>italic</i> text.</p>"
    expected_ansi = "This is \033[3mitalic\033[0m text."
    assert parse_markdown(md_text, 'HTML') == expected_html
    assert parse_markdown(md_text, 'ANSI') == expected_ansi

def test_preformatted_text():
    md_text = "```\nThis text is **preformatted**\n\nAnd can have multiple paragraphs\n```"
    expected_html = "<pre>This text is **preformatted**\n\nAnd can have multiple paragraphs</pre>"
    expected_ansi = "\033[7mThis text is **preformatted**\n\nAnd can have multiple paragraphs\033[0m"
    assert parse_markdown(md_text, 'HTML') == expected_html
    assert parse_markdown(md_text, 'ANSI') == expected_ansi

def test_monospaced_text():
    md_text = "`This is monospaced text.`"
    expected_html = "<p><tt>This is monospaced text.</tt></p>"
    expected_ansi = "\033[7mThis is monospaced text.\033[0m"
    assert parse_markdown(md_text, 'HTML') == expected_html
    assert parse_markdown(md_text, 'ANSI') == expected_ansi

def test_invalid_nested_markup():
    md_text = "**`_this is _`**"
    with pytest.raises(Exception):
        parse_markdown(md_text)

def test_underscore_alone():
    md_text = "_"
    with pytest.raises(Exception):
        parse_markdown(md_text)

def test_underscore_within_quotes():
    md_text = "'_' - теж ок"
    expected_html = "<p>'_' - теж ок</p>"
    expected_ansi = "'_' - теж ок"
    assert parse_markdown(md_text, 'HTML') == expected_html
    assert parse_markdown(md_text, 'ANSI') == expected_ansi

def test_unmatched_markup():
    md_text = "_кінця-краю немає"
    with pytest.raises(Exception):
        parse_markdown(md_text)
