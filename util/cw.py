# -*- coding: <encoding name> -*-

import math
import wave
from util.morse_table import get_cw_table
from util.sequence_generator import ToneSequenceGenerator
from util.sample_source import SampleSource


def calc_paris_bpm(dit_length):
    length = dit_length * 50
    return (5 * 60) / length


class SampleCounter:
    def __init__(self):
        self._count = 0

    def consume(self, samples):
        self._count = self._count + len(samples)

    def count(self):
        return self._count


class SampleWriter:
    def __init__(self, file_handle):
        self._file_handle = file_handle

    def consume(self, samples):
        self._file_handle.writeframes(bytes(samples))


class _CwGen:
    def __init__(self):
        self._sample_source = SampleSource()
        self._sequence_generator = None
        self._num_samples = 0
        self._cw_codes = None

    def _replace_mutual_vowels(self, text):
        text = text.lower()
        mappings = [("!", "."), ("ä", "ae"), ("ö", "oe"), ("ü", "ue"),
                    ("ß", "ss"), ("@", "at"), ("+", "plus")]

        for m in mappings:
            text = text.replace(m[0], m[1])

        return text

    def _remove_unknown_chars(self, text):
        unknown_chars = []

        for char in text:
            if char in self._cw_codes.keys():
                continue
            if char in [" ", "[", "]"]:
                continue
            if char in unknown_chars:
                continue
            unknown_chars.append(char)

        for char in unknown_chars:
            while char in text:
                text = text.replace(char, " ")

        return text

    def _trim_spaces(self, text):
        while "  " in text:
            text = text.replace("  ", " ")
        return text

    def _simplify_text(self, text):
        """ The method first replaces some chars by alternative char
        sequences and replaces characters that are not covered by the
        used alphabet by spaces. Finally sequences of spaces are reduced
        to single spaces."""

        updates = [
            self._replace_mutual_vowels, self._remove_unknown_chars,
            self._trim_spaces
        ]

        for update in updates:
            text = update(text)

        return text

    def dumped(self):
        while plain_text:
            if plain_text[0] == "[":
                index = plain_text.index("]")
                t = plain_text[1:index]
                plain_text = plain_text[index + 1:]
            else:
                t = plain_text[0]
                plain_text = plain_text[1:]
            if t == " ":
                cw_sequence = cw_sequence + "|"
            else:
                if not t in self._cw_codes.keys():
                    raise Exception("Character '" + t +
                                    "' is missing in morse table.")

                cw_sequence = cw_sequence + self._cw_codes[t]
                cw_sequence = cw_sequence + " "
        return cw_sequence

    def _calculate_sample_metrics(self, cw_sequence):
        self._num_samples = 0

        counter = SampleCounter()

        self._sample_source.process_samples(cw_sequence, counter)

        self._num_samples = counter.count()

        self._duration_seconds = self._num_samples / self._sample_source._sampling_rate

    def _write_samples(self, file_handle, cw_sequence):
        self._sample_source.process_samples(cw_sequence,
                                            SampleWriter(file_handle))

    def _write_wav_file(self, file_name, sequence):

        with wave.open(file_name, "wb") as w:
            w.setnframes(self._num_samples)
            w.setnchannels(1)
            w.setsampwidth(1)
            w.setframerate(self._sample_source._sampling_rate)
            self._write_samples(w, sequence)

    def generate(self, text, file_name):
        text = self._simplify_text(text)

        cw_sequence = self._sequence_generator.create_cw_sequence(text)

        self._calculate_sample_metrics(cw_sequence)

        self._write_wav_file(file_name, cw_sequence)

        return self._duration_seconds

    def set_sampling_rate(self, sr):
        self._sample_source.set_sampling_rate(sr)

    def set_len_dit(self, ld):
        self._sample_source.set_len_dit(ld)

    def set_len_separate_char(self, ls):
        self._sample_source.set_len_separate_char(ls)

    def set_len_separate_word(self, ls):
        self._sample_source.set_len_separate_word(ls)

    def set_frequency(self, f):
        self._sample_source.set_frequency(f)

    def set_ramp_time(self, r):
        self._sample_source.set_ramp_time(r)

    def set_cw_codes(self, cw_codes):
        self._sequence_generator = ToneSequenceGenerator(cw_codes)
        self._cw_codes = cw_codes


def create_cw_soundfile(configuration, text, output_filename):

    alphabet = get_cw_table(configuration.get("cw_table"))

    cw_gen = _CwGen()

    defaults = {
        "sampling_rate": 44000,
        "ramp_time": configuration.get("len_dit") / 8,
        "character_gap": configuration.get("len_dit") * 3,
        "word_gap": configuration.get("len_dit") * 6,
        "frequency": 680
    }

    for key in defaults.keys():
        if not key in configuration.keys():
            configuration.set(key, defaults[key])

    cw_gen.set_sampling_rate(configuration.get("sampling_rate"))
    cw_gen.set_len_dit(configuration.get("len_dit"))
    cw_gen.set_len_separate_char(configuration.get("character_gap"))
    cw_gen.set_len_separate_word(configuration.get("word_gap"))
    cw_gen.set_frequency(configuration.get("frequency"))
    cw_gen.set_ramp_time(configuration.get("ramp_time"))
    cw_gen.set_cw_codes(alphabet)

    return cw_gen.generate(text, output_filename)
