import getopt
import getopt
import sys
import winsound

from util.configuration import get_configuration
from util.cw import create_cw_soundfile
from util.morse_table import get_morse_table
from util.rss import get_text_from_feed

if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "a:c:e:f:s:p:", [])

    configuration_name = None
    feed_name = None
    output_filename = None
    text_filename = None
    entry_number = None
    alphabet_file = "alphabet.txt"

    for option in opts:
        if option[0] == "-c":
            configuration_name = option[1]
        if option[0] == "-a":
            alphabet_file = option[1]
        if option[0] == "-f":
            feed_name = option[1]
        if option[0] == "-s":
            output_filename = option[1]
        if option[0] == "-p":
            text_filename = option[1]
        if option[0] == "-e":
            entry_number = option[1]

    if configuration_name is None:
        print("Configuration name is missing (Option '-c')")
        exit(-1)
    if feed_name is None:
        print("Feed URL is missing (Option '-f')")
        exit(-1)
    if output_filename is None:
        print("Output filename is missing (Option '-s')")
        exit(-1)

    configuration = get_configuration(configuration_name)

    try:
        alphabet = get_morse_table(alphabet_file)
    except Exception as ex:
        print("Das Morsealphabet konnte nicht geladen werden:")
        print(ex)
        exit(-1)

    try:
        text = get_text_from_feed(feed_name, entry_number)

        if not text_filename is None:
            with open(text_filename, "w") as file_handle:
                file_handle.write(text)

        create_cw_soundfile(configuration, alphabet, text, output_filename)

        winsound.PlaySound(output_filename, winsound.SND_FILENAME)

    except Exception as ex:
        print(ex)
        exit(-1)
