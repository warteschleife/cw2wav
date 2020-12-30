import yaml


class Configuration:
    def __init__(self):
        with open("cw2wav.yaml", "r") as config_file:
            lines = config_file.readlines()
            text = "".join(lines)
            yaml_content = yaml.load_all(text, Loader=yaml.FullLoader)
            self._config_lookup = {}
            if yaml_content:
                for element in yaml_content:
                    self._config_lookup[element["name"]] = element

    def get_configuration(self, name):

        path = [self._config_lookup[name]]
        path_names = [name]

        while "basis" in path[0].keys():
            parent = path[0]["basis"]
            if parent in path_names:
                raise Exception("Cyclic configuration!")
            path_names.append(parent)
            path = [self._config_lookup[parent]] + path

        result = {}
        for element in path:
            for k in element.keys():
                result[k] = element[k]

        return result
