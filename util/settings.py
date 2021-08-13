# -*- coding: <encoding name> -*-

import yaml


def load_settings(file_name):
    with open(file_name, "r") as config_file:

        lines = config_file.readlines()

        text = "".join(lines)

        yaml_content = yaml.load_all(text, Loader=yaml.FullLoader)

        elements = []

        for element in yaml_content:
            elements.append(element)

        return elements
