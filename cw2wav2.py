# -*- coding: <encoding name> -*-

from ast import arg
import sys
import argparse
from util.player import play_sound
from util.configuration import get_configuration
from util.cw import create_cw_soundfile


def get_time_string(seconds):
    seconds = int(seconds)
    minutes = int(seconds / 60)
    seconds = seconds - minutes * 60
    return str(minutes) + ":" + str(seconds).zfill(2)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Morse Code Generator')
    parser.add_argument("-input",
                        dest="input_file",
                        default="input.txt",
                        help="Input Text File")
    parser.add_argument("-output",
                        dest="output_file",
                        default="output.wav",
                        help="Output File")
    parser.add_argument("-table",
                        dest="cw_table",
                        default="alphabet-full.txt",
                        help="Morse Code Table")
    parser.add_argument("--vvv",
                        dest="send_v",
                        action="store_true",
                        help="Send vvv")
    parser.add_argument("--ct",
                        dest="send_ct",
                        action="store_true",
                        help="Send copy-start")
    parser.add_argument("--ar",
                        dest="send_ar",
                        action="store_true",
                        help="Send end-of-message")
    parser.add_argument("--tone", dest="tone", default="400", help="Frequency")
    parser.add_argument("--dit",
                        dest="dit",
                        default="0.06",
                        help="Length of DIT in seconds")
    parser.add_argument("--chargap",
                        dest="chargap",
                        default="0.6",
                        help="Length of gap between characters in seconds")
    parser.add_argument("--wordgap",
                        dest="wordgap",
                        default="1.2",
                        help="Length of gap between words in seconds")
    parser.add_argument("--play",
                        dest="play",
                        action="store_true",
                        help="Play it directly")
    parser.add_argument("--sample_rate",
                        dest="sample_rate",
                        default="44000",
                        help="Sample Rate")
    parser.add_argument("--ramp_time",
                        dest="ramp_time",
                        default="0.0075",
                        help="Ramp Time")
    args = parser.parse_args()

    with open(args.input_file, "r", encoding="utf8") as textfile:
        text = (" ".join(textfile.readlines())).replace("\n", " ")

        if args.send_ct:
            text = "[CT] " + text

        if args.send_ar:
            text = text + " [AR]"

        if args.send_v:
            text = "vvv " + text

        try:
            duration = create_cw_soundfile(args, text, args.output_file)

            print("Dauer: " + get_time_string(duration))

            if args.play:
                play_sound(args.output_file)
        except Exception as ex:
            print("Error: " + str(ex))
            exit(-1)
