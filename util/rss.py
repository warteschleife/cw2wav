import requests
import xml.sax as sax


class Handler(sax.ContentHandler):
    def __init__(self):
        self._element_stack = []
        self._summary_buffer = ""
        self._title_buffer = ""
        self._summary_stack = None
        self._title_stack = None
        self._entry_stack = None
        self._closing_tag = None
        self._extracted_data = []

    def startDocument(self):
        pass

    def characters(self, text):
        if self._element_stack == self._summary_stack:
            self._summary_buffer = self._summary_buffer + text

        if self._element_stack == self._title_stack:
            self._titel_buffer = self._title_buffer + text

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
            self._extracted_data.append(self._title_buffer.strip())
            self._extracted_data.append(self._summary_buffer.strip())

    def endDocument(self):
        pass

    def get_lines(self):
        return self._extracted_data


def get_text_from_feed(url):
    content = requests.get(url).content

    handler = Handler()

    sax.parseString(content, handler)

    return "\n".join(handler.get_lines())