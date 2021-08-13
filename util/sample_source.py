# -*- coding: <encoding name> -*-

import math
from util.sequence_generator import ToneSequenceGenerator


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


class SampleSource:
    def __init__(self):
        self._sampling_rate = None
        self._len_dit = None
        self._len_separate_char = None
        self._len_separate_word = None
        self._frequency = None
        self._ramp_time = None
        self._tone_dit = None
        self._tone_dah = None
        self._separate_tone = None
        self._separate_char = None
        self._separate_word = None

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

    def _prepare_tones(self):

        len_dah = 3 * self._len_dit

        if self._tone_dit is None:
            self._tone_dit = self._generate_tone(self._len_dit, 100,
                                                 self._ramp_time)

        if self._tone_dah is None:
            self._tone_dah = self._generate_tone(len_dah, 100, self._ramp_time)

        if self._separate_tone is None:
            self._separate_tone = self._generate_tone(self._len_dit, 0, 0)

        if self._separate_char is None:
            self._separate_char = self._generate_tone(self._len_separate_char,
                                                      0, 0)

        if self._separate_word is None:
            self._separate_word = self._generate_tone(self._len_separate_word,
                                                      0, 0)

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

    def process_samples(self, cw_sequence, consumer):
        self._prepare_tones()

        last_sound = False

        for t in cw_sequence:
            if t == ToneSequenceGenerator.DIT:
                if last_sound:
                    consumer.consume(self._separate_tone)
                consumer.consume(self._tone_dit)
                last_sound = True
            elif t == ToneSequenceGenerator.DAH:
                if last_sound:
                    consumer.consume(self._separate_tone)
                consumer.consume(self._tone_dah)
                last_sound = True
            elif t == ToneSequenceGenerator.CHARACTER_GAP:
                consumer.consume(self._separate_char)
                last_sound = False
            elif t == ToneSequenceGenerator.WORD_GAP:
                consumer.consume(self._separate_word)
                last_sound = False
