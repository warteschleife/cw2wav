import math
import wave


class CwGen:
    def __init__(self, configuration, alphabet):

        sampling_rate = configuration["sampling_rate"]

        len_dit = configuration["len_dit"]

        len_separate_char = configuration["character_gap"]

        if not configuration["character_gap"] is None:
            len_separate_char = configuration["character_gap"]
        else:
            len_separate_char = 3 * len_dit

        if not configuration["ramp_time"] is None:
            ramp_time = configuration["ramp_time"]
        else:
            ramp_time = len_dit / 8

        self._frequency = configuration["frequency"]

        len_dah = 3 * len_dit

        print()
        print("Die folgenden Einstellungen werden genutzt:")
        print("-------------------------------------------")
        print("Dauer eines DIT:                       " + str(len_dit) + " s")
        print("Dauer eines DAH:                       " + str(len_dah) + " s")
        print("Zeit zwischen zwei Zeichen:            " +
              str(len_separate_char) + " s")
        print("Dauer der steigenden/fallenden Flanke: " + str(ramp_time) +
              " s")
        print("Samplerate:                            " + str(sampling_rate))
        print("Tonfrequenz:                           " +
              str(self._frequency) + " Hz")

        self._sampling_rate = sampling_rate
        self._tone_dit = self._generate_tone(len_dit, 100, ramp_time)
        self._tone_dah = self._generate_tone(len_dah, 100, ramp_time)
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

    def generate(self, text, file_name):
        text = self._simplyfy(text)
        cw_sequence = self._create_cw_sequence(text)
        signal_sequence_count = self._calculate_sample_count(cw_sequence)
        total_time = signal_sequence_count / self._sampling_rate
        character_count = len(text.replace(" ", ""))

        print()
        print("Details zur Aufnahme:")
        print("---------------------")
        print("Gesamtdauer:        " + self._seconds2minuteAsText(total_time))
        print("Anzahl Zeichen:     " + str(character_count))
        print("Woerter pro Minute: " + str(self.get_wmp()))
        self._write_wav_file(file_name, cw_sequence)
