import math
import wave
from util.morse_table import get_cw_table


def calc_paris_bpm(dit_length):
    length = dit_length * 50
    return (5 * 60) / length


class Envelope:
    def __init__(self, num_samples, rampup_samples):
        self._num_samples = num_samples
        self._rampup_samples = rampup_samples

    def get(self, sample_index):
        if self._rampup_samples == 0:
            return 1
        if sample_index <= self._rampup_samples:
            return sample_index / self._rampup_samples
        elif sample_index >= (self._num_samples - self._rampup_samples):
            return (self._num_samples - sample_index) / self._rampup_samples
        else:
            return 1


class _CwGen:
    def __init__(self):
        self._len_separate_char = 1.8
        self._len_dit = 0.6
        self._ramp_time = self._len_dit / 8
        self._paris_cpm = 0
        self._paris_wmp = 0
        self._tone_dit = 0
        self._tone_dah = 0
        self._separate_tone = None
        self._separate_char = None
        self._separate_word = None
        self._num_samples = 0
        self._frequency = 1

    def _generate_tone(self, duration, volume, ramp_time):
        samples = bytearray()

        samples_per_period = self._sampling_rate / self._frequency

        num_samples = int(self._sampling_rate * duration)

        num_ramp_samples = int(self._sampling_rate * ramp_time)

        envelope = Envelope(num_samples, num_ramp_samples)

        for n in range(num_samples):
            angle = (n / samples_per_period) * 2 * math.pi

            envelope_value = envelope.get(n)

            value = int((math.sin(angle) * volume * envelope_value) + 127)

            samples.append(value)

        return samples

    def _prepare_tones(self):

        len_dah = 3 * self._len_dit

        self._tone_dit = self._generate_tone(self._len_dit, 100,
                                             self._ramp_time)

        self._tone_dah = self._generate_tone(len_dah, 100, self._ramp_time)

        self._separate_tone = self._generate_tone(self._len_dit, 0, 0)

        self._separate_char = self._generate_tone(self._len_separate_char, 0,
                                                  0)

        self._separate_word = self._generate_tone(self._len_separate_word, 0,
                                                  0)

        self._paris_cpm = int(calc_paris_bpm(self._len_dit))

        self._paris_wpm = int(calc_paris_bpm(self._len_dit) / 5)

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

    def _build_word(self, word):
        cw_sequence = ""

        if len(word) == 0:
            return cw_sequence

        if word.startswith("[") and word.endswith("]"):
            return self._cw_codes[word[1:-1]]

        cw_sequence = cw_sequence + self._cw_codes[word[0]]

        for character in word[1:]:
            cw_sequence = cw_sequence + " "
            cw_sequence = cw_sequence + self._cw_codes[character]

        return cw_sequence

    def _create_cw_sequence(self, plain_text):
        words = plain_text.split(" ")

        if len(words) == 0:
            return ""

        cw_sequence = self._build_word(words[0])

        for word in words[1:]:
            cw_sequence = cw_sequence + "|" + self._build_word(word)

        return cw_sequence

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

        for t in cw_sequence:
            if t == ".":
                self._num_samples = self._num_samples + len(self._tone_dit)
                self._num_samples = self._num_samples + len(
                    self._separate_tone)
            elif t == "-":
                self._num_samples = self._num_samples + len(self._tone_dah)
                self._num_samples = self._num_samples + len(
                    self._separate_tone)
            elif t == " ":
                self._num_samples = self._num_samples + len(
                    self._separate_char)
            elif t == "|":
                self._num_samples = self._num_samples + len(
                    self._separate_word)

        self._duration_seconds = self._num_samples / self._sampling_rate

    def _write_samples(self, file_handle, cw_sequence):
        for t in cw_sequence:
            if t == ".":
                file_handle.writeframes(bytes(self._tone_dit))
                file_handle.writeframes(bytes(self._separate_tone))
            elif t == "-":
                file_handle.writeframes(bytes(self._tone_dah))
                file_handle.writeframes(bytes(self._separate_tone))
            elif t == "|":
                file_handle.writeframes(bytes(self._separate_word))
            elif t == " ":
                file_handle.writeframes(bytes(self._separate_char))

    def _write_wav_file(self, file_name, sequence):

        with wave.open(file_name, "wb") as w:
            w.setnframes(self._num_samples)
            w.setnchannels(1)
            w.setsampwidth(1)
            w.setframerate(self._sampling_rate)
            self._write_samples(w, sequence)

    def generate(self, text, file_name):
        self._prepare_tones()

        text = self._simplify_text(text)

        cw_sequence = self._create_cw_sequence(text)

        self._calculate_sample_metrics(cw_sequence)

        self._write_wav_file(file_name, cw_sequence)

        return self._duration_seconds

    def set_sampling_rate(self, sr):
        self._sampling_rate = sr

    def set_len_dit(self, ld):
        self._len_dit = ld

    def set_len_separate_char(self, ls):
        self._len_separate_char = ls

    def set_len_separate_word(self, ls):
        self._len_separate_word = ls

    def set_frequency(self, f):
        self._frequency = f

    def set_ramp_time(self, r):
        self._ramp_time = r

    def set_cw_codes(self, a):
        self._cw_codes = a


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
