import sys
import importlib

winsound_support = False
if importlib.util.find_spec("winsound"):
    import winsound
    winsound_support = True

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

    with open(input_filename, "r", encoding="utf8") as textfile:
        text = (" ".join(textfile.readlines())).replace("\n", "=")

        try:
            duration = create_cw_soundfile(configuration, text,
                                           output_filename)

            print("Dauer: " + get_time_string(duration))

            if winsound_support:
                winsound.PlaySound(output_filename, winsound.SND_FILENAME)
        except Exception as ex:
            print("Error: " + str(ex))
            exit(-1)
