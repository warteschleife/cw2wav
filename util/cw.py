import math
import wave


class CwGen:
    def __init__(self, configuration, alphabet):

        sampling_rate = 44000
        if "sampling_rate" in configuration.keys():
            sampling_rate = configuration["sampling_rate"]

        len_dit = 0.1
        if "len_dit" in configuration.keys():
            len_dit = configuration["len_dit"]

        len_separate_char = 3 * len_dit
        if "len_separate_char" in configuration.keys():
            len_separate_char = configuration["len_separate_char"]

        ramp_time = len_dit / 8
        if "ramp_time" in configuration.keys():
            ramp_time = configuration["ramp_time"]

        self._frequency = 680
        if "frequency" in configuration.keys():
            self._frequency = configuration["frequency"]

        len_dah = 3 * len_dit

        print("The following settings are applied:")
        print("-----------------------------------")
        print("Length of DIT:       " + str(len_dit) + " s")
        print("Length of DAH:       " + str(len_dah) + " s")
        print("Space between chars: " + str(len_separate_char) + " s")
        print("Rising/Falling Time: " + str(ramp_time) + " s")
        print("Sampling Rate:       " + str(sampling_rate))
        print("Frequency:           " + str(self._frequency) + " Hz")

        self._sampling_rate = sampling_rate
        self._tone_dit = self._generate_tone(len_dit, 100, ramp_time)
        self._tone_dah = self._generate_tone(len_dah, 100, ramp_time * 3)
        self._separate_tone = self._generate_tone(len_dit, 0, 0)
        self._separate_char = self._generate_tone(len_separate_char, 0, 0)

        self._alphabet = alphabet

    def _generate_tone(self, duration, volume, ramp_time):
        samples = bytearray()

        samples_per_period = self._sampling_rate / self._frequency

        num_samples = int(self._sampling_rate * duration)

        num_ramp_samples = int(self._sampling_rate * ramp_time)

        for n in range(num_samples):
            angle = (n / samples_per_period) * 2 * math.pi

            if n < num_ramp_samples:
                modulation = n / num_ramp_samples
            elif n > (num_samples - num_ramp_samples):
                modulation = (num_samples - n) / num_ramp_samples
            else:
                modulation = 1

            value = int((math.sin(angle) * volume * modulation) + 127)

            samples.append(value)

        return samples

    def _simplyfy(self, input_text):
        simplified = input_text.lower()
        mappings = [("!", "."), ("ä", "ae"), ("ö", "oe"), ("ü", "ue"),
                    ("ß", "ss"), ("@", "at"), ("+", "plus")]

        for m in mappings:
            simplified = simplified.replace(m[0], m[1])

        chars = []
        for c in simplified:
            if not c in chars:
                chars.append(c)

        for c in chars:
            if not c in self._alphabet.keys():
                print("Character '" + c +
                      "' is unknown. Will replace it by a space.")
                simplified = simplified.replace(c, " ")

        return simplified

    def _create_cw_sequence(self, plain_text):
        cw_sequence = ""

        for t in plain_text:
            if t == " ":
                cw_sequence = cw_sequence + " "
                cw_sequence = cw_sequence + " "
                cw_sequence = cw_sequence + " "
            else:
                if not t in self._alphabet.keys():
                    raise Exception("Character '" + t +
                                    "' is missing in morse table.")

                cw_sequence = cw_sequence + self._alphabet[t]
                cw_sequence = cw_sequence + " "
        return cw_sequence

    def _create_sample_sequence(self, cw_sequence):
        sequence = bytearray()

        for t in cw_sequence:
            if t == ".":
                sequence = sequence + self._tone_dit
                sequence = sequence + self._separate_tone
            elif t == "-":
                sequence = sequence + self._tone_dah
                sequence = sequence + self._separate_tone
            elif t == " ":
                sequence = sequence + self._separate_char

        return sequence

    def _write_wav_file(self, file_name, sequence):

        with wave.open(file_name, "wb") as w:
            w.setnframes(len(sequence))
            w.setnchannels(1)
            w.setsampwidth(1)
            w.setframerate(self._sampling_rate)

            w.writeframes(bytes(sequence))

    def _seconds2minuteAsText(self, total_time_seconds):
        minutes = int(total_time_seconds / 60)
        seconds = int(total_time_seconds - minutes * 60)
        return str(minutes).zfill(2) + ":" + str(seconds).zfill(2)

    def generate(self, text, file_name):
        text = self._simplyfy(text)
        cw_sequence = self._create_cw_sequence(text)
        signal_sequence = self._create_sample_sequence(cw_sequence)
        total_time = len(signal_sequence) / self._sampling_rate
        character_count = len(text.replace(" ", ""))
        print("Gesamtdauer:        " + self._seconds2minuteAsText(total_time))
        print("Anzahl Zeichen:     " + str(character_count))
        print("Woerter pro Minute: " +
              str((character_count * 60 / total_time) / 5))
        self._write_wav_file(file_name, signal_sequence)
