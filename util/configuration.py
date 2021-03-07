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

    return combined_settings