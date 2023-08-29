from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Dict

from bs4 import BeautifulSoup


class WikiParser(HTMLParser):
    def __init__(self, path: str):
        super().__init__()
        self.path = path
        self.tiddler_div_attrs = {'created', 'creator', 'modified', 'modifier',  'tags', 'title'}
        self.soup = self._read_html(self.path)
        self.article_soup = self._get_store_area()
        self.tiddler_list = self._get_tiddlers()

    def add_tiddler(self, new_tiddler_attrs: Dict[str, str], new_tiddler_data: str = ""):
        div_tag = self.soup.new_tag('div')
        for key, value in new_tiddler_attrs.items():
            div_tag[key] = value
        pre_tag = self.soup.new_tag('pre')
        pre_tag.string = new_tiddler_data
        div_tag.append(pre_tag)
        self.article_soup.append(div_tag)
        self.tiddler_list = self._get_tiddlers()
        self._replace_store_area()

    def add_new_tiddlers_from_other_wiki(self, other_wiki):
        this_wiki_tiddlers = self.tiddler_list
        other_wiki_tiddlers = other_wiki.tiddler_list
        this_wiki_titles = [tiddler['title'] for tiddler in this_wiki_tiddlers]
        new_tiddlers = [tiddler for tiddler in other_wiki_tiddlers if tiddler['title'] not in this_wiki_titles]
        for tiddler in new_tiddlers:
            self.add_tiddler(tiddler.attrs, tiddler.text)

    def write_to_file(self):
        with open(self.path, "w", encoding='utf-8') as file:
            file.write(str(self.soup))


    def _read_html(self, path: str) -> BeautifulSoup:
        with open(path, 'r', encoding='utf-8') as html_file:
            feed = html_file.read()
        soup = BeautifulSoup(feed, 'html.parser')
        return soup

    def _get_store_area(self):
        return self.soup.find('div', {'id': 'storeArea'})

    def _replace_store_area(self):
        self._get_store_area().replace_with(self.article_soup)

    def _get_tiddlers(self):
        tiddler_list = []
        for div in self.article_soup.find_all('div'):
            if all(attribute in div.attrs for attribute in self.tiddler_div_attrs):
                tiddler_list.append(div)
        return tiddler_list
