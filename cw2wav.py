# -*- coding: <encoding name> -*-

import sys
from util.player import play_sound
from util.configuration import get_configuration
from util.cw import create_cw_soundfile


def get_time_string(seconds):
    seconds = int(seconds)
    minutes = int(seconds / 60)
    seconds = seconds - minutes * 60
    return str(minutes) + ":" + str(seconds).zfill(2)


if __name__ == "__main__":
    wakeup = False
    copy_start = False
    end_of_message = False

    if "-v" in sys.argv:
        sys.argv.remove("-v")
        wakeup = True

    if "-ct" in sys.argv:
        sys.argv.remove("-ct")
        copy_start = True

    if "-ar" in sys.argv:
        sys.argv.remove("-ar")
        end_of_message = True

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
        text = (" ".join(textfile.readlines())).replace("\n", " ")

        if copy_start:
            text = "[CT] " + text

        if end_of_message:
            text = text + " [AR]"

        if wakeup:
            text = "vvv " + text

        try:
            duration = create_cw_soundfile(configuration, text,
                                           output_filename)

            print("Dauer: " + get_time_string(duration))

            play_sound(output_filename)
        except Exception as ex:
            print("Error: " + str(ex))
            exit(-1)
