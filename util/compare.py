# -*- coding: <encoding name> -*-

import unittest


def count_chars(text):
    result = 0
    for t in text:
        if t == "r":
            result = result + 1
    return result


def compare_parts(text_a, text_b):
    if len(text_a) == 0 and len(text_b) == 0:
        return ("", "")

    possible_result = []

    if len(text_a) < len(text_b):
        result = compare_parts(text_a, text_b[1:])
        possible_result.append((" " + result[0], "m" + result[1]))
    if len(text_a) > 0:
        if text_a[0] == text_b[0]:
            result = compare_parts(text_a[1:], text_b[1:])
            possible_result.append((text_a[0] + result[0], "r" + result[1]))
        else:
            result = compare_parts(text_a[1:], text_b[1:])
            possible_result.append((text_a[0] + result[0], "f" + result[1]))

    result = possible_result[0]
    points = count_chars(result[1])
    for pr in possible_result[1:]:
        pt = count_chars(pr[1])
        if pt > points:
            points = pt
            result = pr
    return result


class TestCompare(unittest.TestCase):
    def test_sample(self):
        self.assertEqual(("abcde", "rrrrr"), compare_parts("abcde", "abcde"))

    def test_missing_char_1(self):
        self.assertEqual((" bcde", "mrrrr"), compare_parts("bcde", "abcde"))

    def test_missing_char_2(self):
        self.assertEqual(("ab de", "rrmrr"), compare_parts("abde", "abcde"))

    def test_missing_char_3(self):
        self.assertEqual(("abcd ", "rrrrm"), compare_parts("abcd", "abcde"))

    def test_missing_char_4(self):
        self.assertEqual(("a cd ", "rmrrm"), compare_parts("acd", "abcde"))

    def test_missing_char_5(self):
        self.assertEqual(("     ", "mmmmm"), compare_parts("", "abcde"))

    def test_invalid_char_1(self):
        self.assertEqual(("xxcde", "ffrrr"), compare_parts("xxcde", "abcde"))


if __name__ == "__main__":
    unittest.main()