import math
import wave


def calc_paris_bpm(dit_length):
    length = dit_length * 50
    return (5 * 60) / length


class _CwGen:
    def __init__(self, configuration, alphabet):
        self._len_separate_char = 1.8
        self._len_dit = 0.6
        self._ramp_time = self._len_dit / 8
        self._paris_cpm = 0
        self._paris_wmp = 0
        self._tone_dit = 0
        self._tone_dah = 0
        self._separate_tone = None
        self._separate_char = None

    def _prepare_tones(self):

        len_dah = 3 * self._len_dit

        self._tone_dit = self._generate_tone(self._len_dit, 100,
                                             self._ramp_time)
        self._tone_dah = self._generate_tone(len_dah, 100, self._ramp_time)
        self._separate_tone = self._generate_tone(self._len_dit, 0, 0)
        self._separate_char = self._generate_tone(self._len_separate_char, 0,
                                                  0)

        self._paris_cpm = int(calc_paris_bpm(self._len_dit))
        self._paris_wpm = int(calc_paris_bpm(self._len_dit) / 5)

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

    def _simplify(self, input_text):
        simplified = input_text.lower()
        mappings = [("!", "."), ("ä", "ae"), ("ö", "oe"), ("ü", "ue"),
                    ("ß", "ss"), ("@", "at"), ("+", "plus")]

        for m in mappings:
            simplified = simplified.replace(m[0], m[1])

        chars = []
        for c in simplified:
            if (not c in chars) and (not c in self._alphabet.keys() and
                                     (not c == ' ')):
                chars.append(c)

        if chars:
            print()
            print(
                "Einige Zeichen stehen nicht als Morsezeichen bereit und werden durch Leerzeichen ersetzt:"
            )

            for c in chars:
                print("- '" + c + "'")
                simplified = simplified.replace(c, " ")

        len_text = len(simplified)
        simplified = simplified.replace("  ", " ")

        while len(simplified) < len_text:
            len_text = len(simplified)
            simplified = simplified.replace("  ", " ")

        return simplified

    def _create_cw_sequence(self, plain_text):
        cw_sequence = ""

        for t in plain_text:
            if t == " ":
                cw_sequence = cw_sequence + " "
                cw_sequence = cw_sequence + " "
            else:
                if not t in self._alphabet.keys():
                    raise Exception("Character '" + t +
                                    "' is missing in morse table.")

                cw_sequence = cw_sequence + self._alphabet[t]
                cw_sequence = cw_sequence + " "
        return cw_sequence

    def _calculate_sample_count(self, cw_sequence):
        num_samples = 0

        for t in cw_sequence:
            if t == ".":
                num_samples = num_samples + len(self._tone_dit)
                num_samples = num_samples + len(self._separate_tone)
            elif t == "-":
                num_samples = num_samples + len(self._tone_dah)
                num_samples = num_samples + len(self._separate_tone)
            elif t == " ":
                num_samples = num_samples + len(self._separate_char)

        return num_samples

    def _write_samples(self, file_handle, cw_sequence):
        for t in cw_sequence:
            if t == ".":
                file_handle.writeframes(bytes(self._tone_dit))
                file_handle.writeframes(bytes(self._separate_tone))
            elif t == "-":
                file_handle.writeframes(bytes(self._tone_dah))
                file_handle.writeframes(bytes(self._separate_tone))
            elif t == " ":
                file_handle.writeframes(bytes(self._separate_char))

    def _write_wav_file(self, file_name, sequence):

        with wave.open(file_name, "wb") as w:
            w.setnframes(self._calculate_sample_count(sequence))
            w.setnchannels(1)
            w.setsampwidth(1)
            w.setframerate(self._sampling_rate)
            self._write_samples(w, sequence)

    def _seconds2minuteAsText(self, total_time_seconds):
        minutes = int(total_time_seconds / 60)
        seconds = int(total_time_seconds - minutes * 60)
        return str(minutes).zfill(2) + ":" + str(seconds).zfill(2)

    def get_wmp(self):
        cw_sequence = self._create_cw_sequence("paris")
        signal_sequence_count = self._calculate_sample_count(cw_sequence)
        total_time = signal_sequence_count / self._sampling_rate
        return 60 / total_time

    def get_bpm(self):
        return self.get_wmp() * 5

    def generate(self, text, file_name):
        self._prepare_tones()
        text = self._simplify(text)
        cw_sequence = self._create_cw_sequence(text)
        signal_sequence_count = self._calculate_sample_count(cw_sequence)
        total_time = signal_sequence_count / self._sampling_rate
        character_count = len(text.replace(" ", ""))

        print()
        print("Details zur Aufnahme:")
        print("---------------------")
        print("Gesamtdauer:                " +
              self._seconds2minuteAsText(total_time))
        print("Anzahl Zeichen:             " + str(character_count))
        print("Zeichen pro Minute:         " +
              str(60 * character_count / total_time))
        print("Woerter pro Minute:         " + str(self.get_wmp()))
        print("Zeichen pro Minute (PARIS): " + str(self._paris_cpm))
        print("Woerter pro Minute (PARIS): " + str(self._paris_wpm))
        self._write_wav_file(file_name, cw_sequence)

    def set_sampling_rate(self, sr):
        self._sampling_rate = sr

    def set_len_dit(self, ld):
        self._len_dit = ld

    def set_len_separate_char(self, ls):
        self._len_separate_char = ls

    def set_frequency(self, f):
        self._frequency = f

    def set_ramp_time(self, r):
        self._ramp_time = r

    def set_alphabet(self, a):
        self._alphabet = a


def create_cw_soundfile(configuration, alphabet, text, output_filename):
    cw_gen = _CwGen(configuration, alphabet)

    cw_gen.set_sampling_rate(configuration["sampling_rate"])
    cw_gen.set_len_dit(configuration["len_dit"])
    cw_gen.set_len_separate_char(configuration["character_gap"])
    cw_gen.set_frequency(configuration["frequency"])

    if configuration["ramp_time"]:
        cw_gen.set_ramp_time(configuration["ramp_time"])
    else:
        cw_gen.set_ramp_time(configuration["len_dit"] / 8)

    cw_gen.set_alphabet(alphabet)

    cw_gen.generate(text, output_filename)
