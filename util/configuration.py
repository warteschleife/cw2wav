import yaml


class Configuration:
    def __init__(self, default_settings):
        with open("cw2wav.yaml", "r") as config_file:

            self._default_settings = default_settings

            lines = config_file.readlines()

            text = "".join(lines)

            yaml_content = yaml.load_all(text, Loader=yaml.FullLoader)

            self._config_lookup = {}

            if yaml_content:
                for element in yaml_content:
                    self._config_lookup[element["name"]] = element

    def _get_inheritance_path(self, name):

        if not name in self._config_lookup.keys():
            raise Exception("Die ausgewählte Konfiguration '" + name +
                            "' existiert nicht.")

        configurations = [self._config_lookup[name]]

        path_names = [name]

        while "basis" in configurations[0].keys():
            parent = configurations[0]["basis"]

            if parent in path_names:
                raise Exception("Cyclic configuration!")

            path_names.append(parent)

            if not parent in self._config_lookup.keys():
                raise Exception(
                    "Konfiguration '" + configurations[0]["name"] +
                    "' referenziert eine nicht existierende Konfiguration mit dem Namen '"
                    + parent + "'.")

            configurations = [self._config_lookup[parent]] + configurations

        return configurations

    def get_configuration(self, name):
        path = self._get_inheritance_path(name)

        sources = {}

        result = dict(self._default_settings)

        for element_name in result.keys():
            sources[element_name] = "builtin"

        for element in path:
            configuration_name = element["name"]

            for parameter_name in element.keys():
                if parameter_name == "name":
                    continue

                if parameter_name == "basis":
                    continue

                result[parameter_name] = element[parameter_name]

                sources[parameter_name] = configuration_name

        print()
        print(
            "Anhand der Konfigurationsdatei wurden folgende Einstellungen vorgenommen:"
        )
        print(
            "-------------------------------------------------------------------------"
        )

        for k in sorted(result.keys()):
            source_info = ""

            if not name == sources[k]:
                source_info = " Quelle: '" + sources[k] + "'."

            print("Parameter '" + k + "' wird auf den Wert '" +
                  str(result[k]) + "' gesetzt." + source_info)

        return result
