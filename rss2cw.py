import sys
import winsound

from util.configuration import get_configuration
from util.cw import create_cw_soundfile
from util.morse_table import get_morse_table
from util.rss import get_text_from_feed

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(
            "Der Aufruf benötigt die Parameter 'Konfigurationsname', 'Feed URL', 'Ausgabedatei'."
        )
        exit(-1)

    configuration_name = sys.argv[1]
    feed_name = sys.argv[2]
    output_filename = sys.argv[3]
    text_filename = None

    if len(sys.argv) > 4:
        text_filename = sys.argv[4]

    configuration = get_configuration(configuration_name)

    try:
        alphabet = get_morse_table("alphabet.txt")
    except Exception as ex:
        print("Das Morsealphabet konnte nicht geladen werden:")
        print(ex)
        exit(-1)

    try:
        text = get_text_from_feed(feed_name)

        if not text_filename is None:
            with open(text_filename, "w") as file_handle:
                file_handle.write(text)

        create_cw_soundfile(configuration, alphabet, text, output_filename)

        winsound.PlaySound(output_filename, winsound.SND_FILENAME)

    except Exception as ex:
        print(ex)
        exit(-1)
