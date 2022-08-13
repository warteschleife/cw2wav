# -*- coding: <encoding name> -*-

import wave
from util.morse_table import get_cw_table
from util.sequence_generator import ToneSequenceGenerator
from util.sample_source import SampleSource


def calc_paris_bpm(dit_length):
    length = dit_length * 50
    return (5 * 60) / length


class SampleWriter:
    def __init__(self, file_handle):
        self._file_handle = file_handle

    def consume(self, samples):
        self._file_handle.writeframes(bytes(samples))


class _CwGen:
    def __init__(self):
        self._sample_source = SampleSource()
        self._sequence_generator = None
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

    def _write_wav_file(self, file_name, sequence):
        num_samples = self._sample_source.get_sample_count(sequence)

        with wave.open(file_name, "wb") as file_handle:
            file_handle.setnframes(num_samples)
            file_handle.setnchannels(1)
            file_handle.setsampwidth(1)
            file_handle.setframerate(self._sample_source._sampling_rate)

            self._sample_source.process_samples(sequence,
                                                SampleWriter(file_handle))

            return num_samples

    def generate(self, text, file_name):
        text = self._simplify_text(text)

        cw_sequence = self._sequence_generator.create_cw_sequence(text)

        num_samples = self._write_wav_file(file_name, cw_sequence)

        return num_samples / self._sample_source._sampling_rate

    def set_sample_source(self, sample_source):
        self._sample_source = sample_source

    def set_cw_codes(self, cw_codes):
        self._sequence_generator = ToneSequenceGenerator(cw_codes)
        self._cw_codes = cw_codes


def get_initialized_sample_source(configuration):
    sample_source = SampleSource()

    sample_source.set_sampling_rate(float(configuration.sample_rate))
    sample_source.set_len_dit(float(configuration.dit))
    sample_source.set_len_separate_char(float(configuration.chargap))
    sample_source.set_len_separate_word(float(configuration.wordgap))
    sample_source.set_frequency(float(configuration.tone))
    sample_source.set_ramp_time(float(configuration.ramp_time))

    return sample_source


def add_default_settings(configuration):
    """ Checks the configuration for mandatory key-value-pairs and adds default values when keys are missing. """
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


def create_cw_soundfile(configuration, text, output_filename):

    sample_source = get_initialized_sample_source(configuration)

    cw_gen = _CwGen()

    cw_gen.set_sample_source(sample_source)

    alphabet = get_cw_table(configuration.cw_table)

    cw_gen.set_cw_codes(alphabet)

    return cw_gen.generate(text, output_filename)
