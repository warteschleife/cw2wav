import sys

import winsound

from util.morse_table import get_morse_table
from util.configuration import get_configuration
from util.cw import create_cw_soundfile


def get_time_string(seconds):
    seconds = int(seconds)
    minutes = int(seconds / 60)
    seconds = seconds - minutes * 60
    return str(minutes) + ":" + str(seconds).zfill(2)


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
            duration = create_cw_soundfile(configuration, alphabet, text,
                                           output_filename)

            print("Dauer: " + get_time_string(duration))

            winsound.PlaySound(output_filename, winsound.SND_FILENAME)
        except Exception as ex:
            print("Error: " + ex)
            exit(-1)
