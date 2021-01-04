import sys, random, util
from util import morse_table
from util import compare

ALPHABET_FILE = "alphabet.txt"
HISTORY_FILE = "training_history.txt"
TEST_FILE = "training_testfile.txt"
RESULT_FILE = "training_resultfile.txt"


def generate_test(char_weights):
    char_source = "".join(
        list(map(lambda x: x * char_weights[x], char_weights.keys())))

    test = []

    for _ in range(5):
        line = ""

        for _ in range(10):
            line = line + char_source[random.randrange(0, len(char_source))]

        test.append(line)

    return test


def store_in_history(test_content, end_marker):
    with open(HISTORY_FILE, "a") as history_file:
        history_file.write(" ".join(test_content).strip() + end_marker)


def read_resultfile():
    try:
        with open(RESULT_FILE, "r") as result_file:
            return list(map(lambda x: x.strip(), result_file.readlines()))
    except:
        return None


def store_testfile(content, file_name=TEST_FILE):
    with open(file_name, "w") as test_file:
        for line in content:
            test_file.write(line + "\n")


def get_last_stored_result():
    last_stored_result = []
    with open(HISTORY_FILE, "r") as history_file:
        line = history_file.readline()
        while line:
            parts = line.split("|")
            if len(parts[1]) > 0:
                last_stored_result = list(
                    map(lambda x: x.strip(), parts[1].split(" ")))
            line = history_file.readline()
    return last_stored_result


def calculate_char_weights():
    global alphabet

    weights = {}

    for letter in alphabet.keys():
        weights[letter] = 1

    with open(HISTORY_FILE, "r") as history_file:
        line = history_file.readline()
        while line:
            mistakes_in_test = 0
            parts = line.split("|")

            given_text = list(map(lambda x: x.strip(), parts[0].split(" ")))
            read_text = list(map(lambda x: x.strip(), parts[1].split(" ")))

            for index in range(len(given_text)):

                result = compare.compare_parts(read_text[index],
                                               given_text[index])

                marks = enumerate(result[1])
                mistakes_in_test = mistakes_in_test + len(result[1].replace(
                    "r", ""))
                for enumerated_mark in marks:
                    mark = enumerated_mark[1]

                    position = enumerated_mark[0]

                    letter = given_text[index][position]

                    if mark == "m" or mark == "f":
                        weights[letter] = weights[letter] + 2
                    elif mark == "r":
                        if weights[letter] > 1:
                            weights[letter] = weights[letter] - 1
                    else:
                        raise Exception()

            line = history_file.readline()
            print("Mistakes: " + str(mistakes_in_test))
    return weights


def dump(char_weights):
    weight_list = list(map(lambda x: (x, char_weights[x]),
                           char_weights.keys()))

    weight_list = list(
        enumerate(list(sorted(weight_list, key=lambda x: x[1], reverse=True))))

    if len(weight_list) <= 20:
        for element in weight_list:
            print(
                str(element[0]) + ". '" + (element[1][0] * element[1][1]) +
                "'")
    else:
        for element in weight_list[:10]:
            print(str(element[0]) + ". '" + (element[1][0] * element[1][1]))
        for element in weight_list[-10:]:
            print(str(element[0]) + ". '" + (element[1][0] * element[1][1]))


alphabet = morse_table.get_morse_table(ALPHABET_FILE)

result = read_resultfile()

if result is None:
    print("Initialized Training Environment")
    weight = {}
    for letter in alphabet.keys():
        weight[letter] = 1
    test = generate_test(weight)

    with open(HISTORY_FILE, "w"):
        pass

    store_in_history(test, "|")

    store_testfile(test)

    store_testfile(test, RESULT_FILE)

    exit()

else:

    last_result = get_last_stored_result()

    if "#".join(last_result) == "#".join(result):
        print("Seems like the test has not been performed.")
        exit()

    store_in_history(result, "\n")

    char_weights = calculate_char_weights()

    dump(char_weights)

    test = generate_test(char_weights)

    store_in_history(test, "|")

    store_testfile(test)
