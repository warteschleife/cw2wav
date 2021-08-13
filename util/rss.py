# -*- coding: <encoding name> -*-

import requests
import xml.sax as sax


class _RssAtomHandler(sax.ContentHandler):
    """ This class should be able to parse RSS feeds as well as Atom feeds (at least some).
    It just extracts the title and the summary/description of the feeds entries. """
    def __init__(self):
        self._element_stack = []
        self._summary_buffer = ""
        self._title_buffer = ""
        self._summary_stack = None
        self._title_stack = None
        self._entry_stack = None
        self._closing_tag = None
        self._extracted_data = []

    def characters(self, text):
        if self._element_stack == self._summary_stack:
            self._summary_buffer = self._summary_buffer + text

        if self._element_stack == self._title_stack:
            self._title_buffer = self._title_buffer + text

    def startElement(self, name, attributes):
        if self._summary_stack is None:
            if name == "feed":
                self._summary_stack = ["feed", "entry", "summary"]
                self._title_stack = ["feed", "entry", "title"]
                self._entry_stack = ["feed", "entry"]
                self._closing_tag = "entry"
            elif name == "rss":
                self._summary_stack = ["rss", "channel", "item", "description"]
                self._title_stack = ["rss", "channel", "item", "title"]
                self._entry_stack = [
                    "rss",
                    "channel",
                    "item",
                ]
                self._closing_tag = "item"

        self._element_stack.append(name)

        if self._element_stack == self._entry_stack:
            self._summary_buffer = ""
            self._title_buffer = ""

    def endElement(self, name):
        self._element_stack = self._element_stack[:-1]

        if name == self._closing_tag:
            self._extracted_data.append(
                (self._title_buffer.strip(), self._summary_buffer.strip()))

    def get_lines(self, entry_number=None):
        result_list = self._extracted_data
        if not entry_number is None:
            number = int(int(entry_number) - 1)
            result_list = [self._extracted_data[number]]
        lines = []
        for entry in result_list:
            lines.append(entry[0])
            lines.append(entry[1])
        return lines


def get_text_from_feed(url, entry_number=None):
    """ The function returns the content of the feed that is selected by 'url' """

    content = requests.get(url).content

    handler = _RssAtomHandler()

    sax.parseString(content, handler)

    return "\n".join(handler.get_lines(entry_number))