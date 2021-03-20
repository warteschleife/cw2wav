import sys, random, util
from util import morse_table
from util.configuration import get_configuration

configuration = get_configuration()

alphabet_filename = configuration.get("cw_table")

alphabet = morse_table.get_cw_table(alphabet_filename)

characters = list(alphabet.keys())

with open(sys.argv[1], "w") as random_text:
    for _ in range(5):
        for _ in range(5):
            random_text.write(characters[random.randrange(0, len(characters))])
        random_text.write("\n")
