import sys

import winsound

from util.morse_table import get_morse_table
from util.configuration import get_configuration
from util.cw import create_cw_soundfile

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(
            "Der Aufruf benötigt die Parameter 'Konfigurationsname', 'Inputdatei', 'Ausgabedatei'."
        )
        exit(-1)

    configuration_name = sys.argv[1]
    input_filename = sys.argv[2]
    output_filename = sys.argv[3]

    configuration = get_configuration(configuration_name)

    try:
        alphabet = get_morse_table("alphabet.txt")
    except Exception as ex:
        print("Das Morsealphabet konnte nicht geladen werden:")
        print(ex)
        exit(-1)

    with open(input_filename, "r", encoding="utf8") as textfile:
        text = (" ".join(textfile.readlines())).replace("\n", "=")

        try:
            create_cw_soundfile(configuration, alphabet, text, output_filename)

            winsound.PlaySound(output_filename, winsound.SND_FILENAME)
        except Exception as ex:
            print(ex)
            exit(-1)
