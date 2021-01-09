import sys
import requests
import xml.sax as sax
import winsound

from util import morse_table
from util import configuration
from util.cw import CwGen


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
        return "\n".join(self._extracted_data)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(
            "Der Aufruf benötigt die Parameter 'Konfigurationsname', 'Feed URL', 'Ausgabedatei'."
        )
        exit(-1)

    configuration_name = sys.argv[1]
    feed_name = sys.argv[2]
    output_filename = sys.argv[3]

    parameters = {
        "sampling_rate": 44000,
        "len_dit": 0.1,
        "ramp_time": None,
        "frequency": 680
    }

    configuration = configuration.Configuration(parameters)

    try:
        alphabet = morse_table.get_morse_table("alphabet.txt")
    except Exception as ex:
        print("Das Morsealphabet konnte nicht geladen werden:")
        print(ex)
        exit(-1)

    try:
        content = requests.get(feed_name).content

        handler = Handler()

        sax.parseString(content, handler)

        cw_gen = CwGen(configuration.get_configuration(configuration_name),
                       alphabet)
        cw_gen.generate(handler.get_lines(), output_filename)

        winsound.PlaySound(output_filename, winsound.SND_FILENAME)
    except Exception as ex:
        print(ex)
        exit(-1)
