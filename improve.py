import sys, random, util
from util import morse_table
from util import compare

alphabet = morse_table.get_morse_table("alphabet.txt")

test_file = None
result_file = None
history_file = None


def get_content(file_name):
    try:
        with open(file_name, "r") as file_handle:
            return list(map(lambda x: x.strip(), file_handle.readlines()))
    except:
        return None


def print_training_plan(statistic):
    results = []
    for x in statistic.keys():
        results.append((x, statistic[x]))
    results = list(sorted(results, key=lambda x: x[1]))
    header = ""
    count = ""
    for r in results:
        header = header + r[0].rjust(3)
        count = count + str(r[1]).rjust(3)
    print(header)
    print(count)


def compare_results(actual, expected):
    mistakes = 0
    if len(actual) == len(expected):
        for index in range(len(actual)):
            result = compare.compare_parts(actual[index], expected[index])
            print()
            print(expected[index])
            print(result[0])
            print(result[1].replace("r", " ").replace("m", " "))
            mistakes = mistakes + len(result[1].replace("r", ""))
    else:
        print("Cannot compare results.")

    print("Total mistakes: " + str(mistakes))


test_file = get_content("random.txt")
result_file = get_content("result.txt")

if not result_file is None:
    if len(test_file) == len(result_file):
        line = " ".join(test_file) + " " + " ".join(result_file) + "\n"
        with open("history.txt", "a") as history:
            history.write(line)
    compare_results(result_file, test_file)

statistic = {}
for k in alphabet.keys():
    statistic[k] = 2

with open("history.txt", "r") as history:
    line = history.readline()
    while line:
        elements = list(map(lambda x: x.strip(), line.split(" ")))
        for index in range(int(len(elements) / 2)):
            expected_result = elements[index]
            actual_result = elements[index + int(len(elements) / 2)]
            compare_result = compare.compare_parts(actual_result,
                                                   expected_result)
            mistakes = compare_result[1]
            while expected_result:
                if mistakes[0] == "f" or mistakes[0] == "m":
                    if expected_result[0] in statistic.keys():
                        if statistic[expected_result[0]] < 20:
                            statistic[expected_result[0]] = statistic[
                                expected_result[0]] + 2
                    else:
                        statistic[expected_result[0]] = 2
                else:
                    if expected_result[0] in statistic.keys():
                        if statistic[expected_result[0]] > 1:
                            statistic[expected_result[0]] = statistic[
                                expected_result[0]] - 1
                    else:
                        statistic[expected_result[0]] = 1

                mistakes = mistakes[1:]
                expected_result = expected_result[1:]
        line = history.readline()

characters = []
for k in statistic.keys():
    for _ in range(statistic[k]):
        characters.append(k)

print_training_plan(statistic)

with open("random.txt", "w") as random_text:
    for _ in range(5):
        for _ in range(10):
            random_text.write(characters[random.randrange(0, len(characters))])
        random_text.write("\n")
