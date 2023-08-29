import pytest

from html_parser import WikiParser


def test_find_new_tiddlers() -> None:
    old_wiki = WikiParser("./test_data/old_wiki.html")
    new_wiki = WikiParser("./test_data/new_wiki.html")

    assert len(old_wiki.tiddler_list) == 1
    assert len(new_wiki.tiddler_list) == 2
    assert set(div.attrs['title'] for div in new_wiki.tiddler_list) == {"old_div", "new_div"}


def test_add_tiddler() -> None:
    old_wiki = WikiParser("./test_data/old_wiki.html")


    new_tiddler_attributes = {
        "created": "19990101111528345",
        "creator": "test",
        "modified": "19990101111528345",
        "modifier": "test",
        "title": "generated_div",
        "tags": ""
    }

    old_wiki.add_tiddler(new_tiddler_attributes, "")

    updated_articles = old_wiki.article_soup

    assert len(old_wiki.tiddler_list) == 2
    assert set(div.attrs['title'] for div in old_wiki.tiddler_list) == {"old_div", "generated_div"}


def test_add_new_tiddlers_from_other_wiki() -> None:
    old_wiki = WikiParser("./test_data/old_wiki.html")
    new_wiki = WikiParser("./test_data/new_wiki.html")

    old_wiki.add_new_tiddlers_from_other_wiki(new_wiki)

    assert len(old_wiki.tiddler_list) == 2
    assert set(div.attrs['title'] for div in old_wiki.tiddler_list) == {"old_div", "new_div"}
