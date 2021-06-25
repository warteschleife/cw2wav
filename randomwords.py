import sys, random, os
from util import morse_table

if len(sys.argv) != 3:
    print("python randomwords.py [alphabet-file] [output-file]")
    exit()

alphabet_filename = sys.argv[1]

output_filename = sys.argv[2]

if not os.path.exists(alphabet_filename):
    print("Alphabet file does not exist: '" + alphabet_filename + "'")
    exit()

if os.path.exists(output_filename):
    print("File already exist: '" + output_filename + "'")
    exit()

alphabet = morse_table.get_cw_table(alphabet_filename)

characters = list(filter(lambda x: len(x) == 1, alphabet.keys()))

info_string = "Random word created out of the following characters: "

character_list = ", ".join(map(lambda x: "'" + x + "'", characters))

print(info_string + character_list)

with open(sys.argv[1], "w") as output_filename:
    for _ in range(5):
        for _ in range(5):
            output_filename.write(characters[random.randrange(
                0, len(characters))])
        output_filename.write("\n")
