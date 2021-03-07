import util.settings
import random
import re


def combine_configuration(settings, name):
    combined_setup = {}

    while name:
        element = settings[name]

        for key in element.keys():
            if key in ["name", "base"]:
                continue
            if key in combined_setup.keys():
                continue
            combined_setup[key] = element[key]

        if "base" in element.keys():
            name = element["base"]
        else:
            name = None
    return combined_setup


def replace_range_by_random(text):
    elements = re.match("(\\d+)-(\\d+)", str(text))

    if elements:
        lower = int(elements.group(1))
        higher = int(elements.group(2))
        selected = random.randrange(lower, higher)
        return selected

    return text


def get_configuration(name):
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