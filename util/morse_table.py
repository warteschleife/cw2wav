import re

# Check https://morsecode.world/international/morse.html


def get_cw_table(file_name):
    result = {}
    with open(file_name, "r") as morse_table:
        for line in morse_table.readlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue
            elements = re.match("^(\\S+)\\s+([\\.-]+)$", line)
            if elements:
                key = elements.group(1).lower()
                pattern = elements.group(2).lower()

                if key in result.keys():
                    raise Exception("Duplicate definition for character '" +
                                    key + "'")
                result[key] = pattern
            else:
                raise Exception("Invalid line in '" + file_name + "': \"" +
                                line + "\"")
    return result
