# -*- coding: <encoding name> -*-

import util.settings
import random
import re


def combine_configuration(settings, name):

    BASE_TAG = "base"

    inheritance_path = []

    while name:
        if name in inheritance_path:
            raise Exception("Cyclic inheritance detected in configuration")
        inheritance_path.append(name)

        if BASE_TAG in settings[name].keys():
            name = settings[name][BASE_TAG]
        else:
            name = None

    combined_setup = {}

    for name in inheritance_path:
        element = settings[name]

        for key in element.keys():
            if key == BASE_TAG:
                continue
            if key in combined_setup.keys():
                continue
            combined_setup[key] = element[key]

    return combined_setup


def replace_range_by_random(text):
    elements = re.match("(\\d+)-(\\d+)", str(text))

    if elements:
        lower = int(elements.group(1))
        higher = int(elements.group(2))
        selected = random.randrange(lower, higher)
        return selected

    return text


class DictWrapper:
    def __init__(self, name, dictionary):
        self._name = name
        self._dictionary = dictionary

    def set(self, name, value):
        self._dictionary[name] = value

    def get(self, name):
        if name in self._dictionary.keys():
            return self._dictionary[name]
        else:
            raise Exception("'" + name +
                            "' is undefined in the configuration '" +
                            self._name + "'.")

    def keys(self):
        return self._dictionary.keys()


def get_configuration(name="default"):
    settings = util.settings.load_settings("cw2wav.yaml")[0]

    if not name in settings.keys():
        print("A configuration '" + name +
              "' does not exist in 'cw2wav.yaml'.")
        exit()

    combined_settings = combine_configuration(settings, name)

    if "frequency" in combined_settings.keys():
        combined_settings["frequency"] = replace_range_by_random(
            combined_settings["frequency"])

    return DictWrapper(name, combined_settings)