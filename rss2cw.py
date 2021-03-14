# TODO: Clean up!

import getopt
import getopt
import re
import sys
import winsound
import yaml
import os

from util.configuration import get_configuration
from util.cw import create_cw_soundfile
from util.morse_table import get_cw_table
from util.rss import get_text_from_feed


def get_tmp_file_identifier(basepatterns):
    """ This function returns an identifier for file name that is not in use
    in the current directory. """
    id = 1
    for name in os.listdir():
        for pattern in basepatterns:
            regex = "^" + pattern[0] + "(\\d+)" + pattern[1] + "$"
            reresult = re.match(regex, name)
            if reresult:
                number = int(reresult.group(1))
                if number >= id:
                    id = number + 1
    return str(id).zfill(10)


feeds = {}

try:

    with open("feeds.yaml", "r") as feed_file:

        lines = feed_file.readlines()

        text = "".join(lines)
except:
    print("The file 'feeds.yaml' couldn't be read. Is it missing?")
    exit(-1)

yaml_content = yaml.load_all(text, Loader=yaml.FullLoader)

if yaml_content:
    for yaml_part in yaml_content:
        for feed_name in yaml_part.keys():
            feeds[feed_name] = yaml_part[feed_name]

if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "a:c:e:f:s:p:hn", [])

    output_file_identifier = get_tmp_file_identifier([("tmp-", ".wav"),
                                                      ("tmp-", ".txt")])

    configuration_name = "default"
    feed_name = None
    output_filename = "tmp-" + output_file_identifier + ".wav"
    text_filename = "tmp-" + output_file_identifier + ".txt"
    entry_number = None
    help_requested = False
    play_sound = True

    for option in opts:
        if option[0] == "-c":
            configuration_name = option[1]
        if option[0] == "-a":
            alphabet_file = option[1]
        if option[0] == "-f":
            feed_url = feeds["feeds"][option[1]]["url"]
        if option[0] == "-s":
            output_filename = option[1]
        if option[0] == "-p":
            text_filename = option[1]
        if option[0] == "-e":
            entry_number = option[1]
        if option[0] == "-h":
            help_requested = True
        if option[0] == "-n":
            play_sound = False

    if help_requested:
        feednames = sorted(feeds["feeds"].keys())
        for name in feednames:
            print("- " + name)

    if configuration_name is None:
        print("Configuration name is missing (Option '-c')")
        exit(-1)

    configuration = get_configuration(configuration_name)

    text = get_text_from_feed(feed_url, entry_number)

    if not text_filename is None:
        with open(text_filename, "w") as file_handle:
            file_handle.write(text)

    create_cw_soundfile(configuration, text, output_filename)

    if play_sound:
        winsound.PlaySound(output_filename, winsound.SND_FILENAME)
