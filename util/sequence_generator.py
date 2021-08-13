# -*- coding: <encoding name> -*-


class ToneSequenceGenerator:
    DIT = "."
    DAH = "-"
    CHARACTER_GAP = " "
    WORD_GAP = "|"

    def __init__(self, cw_codes):
        expected_chars = [ToneSequenceGenerator.DIT, ToneSequenceGenerator.DAH]
        for character in cw_codes.keys():
            for element in cw_codes[character]:
                if not element in expected_chars:
                    raise Exception(
                        "Invalid alphabet definition for character '" +
                        character + "'")

        self._cw_codes = cw_codes

    def _build_word(self, word):
        cw_sequence = ""

        if len(word) == 0:
            return cw_sequence

        if word.startswith("[") and word.endswith("]"):
            return self._cw_codes[word[1:-1]]

        cw_sequence = cw_sequence + self._cw_codes[word[0]]

        for character in word[1:]:
            cw_sequence = cw_sequence + ToneSequenceGenerator.CHARACTER_GAP
            cw_sequence = cw_sequence + self._cw_codes[character]

        return cw_sequence

    def create_cw_sequence(self, plain_text):
        words = plain_text.split(" ")

        if len(words) == 0:
            return ""

        cw_sequence = self._build_word(words[0])

        for word in words[1:]:
            cw_sequence = cw_sequence + ToneSequenceGenerator.WORD_GAP + self._build_word(
                word)

        return cw_sequence
