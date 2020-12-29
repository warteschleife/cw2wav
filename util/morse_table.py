import re


def get_morse_table(file_name):
    result = {}
    with open("alphabet.txt", "r") as morse_table:
        for line in morse_table.readlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue
            elements = re.match("^(\\S)\\s+([\\.-]+)$", line)
            if elements:
                if elements.group(1) in result.keys():
                    raise Exception("Duplicate definition for character '" +
                                    elements.group(1) + "'")
                result[elements.group(1)] = elements.group(2)
            else:
                raise Exception("Invalid line in '" + file_name + "': \"" +
                                line + "\"")
    return result
