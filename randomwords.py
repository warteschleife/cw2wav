import sys, random, util
from util import morse_table
alphabet = morse_table.get_morse_table("alphabet.txt")

characters = list(alphabet.keys())

with open(sys.argv[1], "w") as random_text:
    for _ in range(10):
        for _ in range(5):
            random_text.write(characters[random.randrange(0, len(characters))])
        random_text.write("\n")
