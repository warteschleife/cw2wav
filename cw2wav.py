import sys

import winsound

from util import morse_table
from util import configuration
from util.cw import CwGen

if __name__ == "__main__":
    if len(sys.argv) < 4:
        exit()

    configuration = configuration.Configuration()

    try:
        alphabet = morse_table.get_morse_table("alphabet.txt")
    except Exception as ex:
        print(ex)
        exit(-1)

    with open(sys.argv[2], "r", encoding="utf8") as textfile:
        text = "vvv  " + (" ".join(textfile.readlines())).replace("\n", "=")

        cw_gen = CwGen(configuration.get_configuration(sys.argv[1]), alphabet)

        try:
            cw_gen.generate(text, sys.argv[3])
        except Exception as ex:
            print(ex)
            exit(-1)

        winsound.PlaySound(sys.argv[3], winsound.SND_FILENAME)
