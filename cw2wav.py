import wave, math, random, winsound, struct, sys


class CwGen:
    def __init__(self):
        self._dit_ms = 0.1
        self._dah_ms = 3 * self._dit_ms
        self._ramp_ms = (self._dit_ms / 5)

        self._alphabet = {
            'a': ".-",
            'b': "-...",
            'c': "-.-.",
            'd': "-..",
            'e': ".",
            'f': "..-.",
            'g': "--.",
            'h': "....",
            'i': "..",
            'j': ".---",
            'k': "-.-",
            'l': ".-..",
            'm': "--",
            'n': "-.",
            'o': "---",
            'p': ".--.",
            'q': "--.-",
            'r': ".-.",
            's': "...",
            't': "-",
            'u': "..-",
            'v': "...-",
            'w': ".--",
            'x': "-..-",
            'y': "-.--",
            'z': "--..",
            '0': "-----",
            '1': ".----",
            '2': "..---",
            '3': "...--",
            '4': "....-",
            '5': ".....",
            '6': "-....",
            '7': "--...",
            '8': "---..",
            '9': "----.",
            '?': "..--..",
            ',': "--..--",
            '.': ".-.-.-",
            '=': "-...-"
        }

    def _simplyfy(self, input_text):
        simplified = input_text.lower()
        mappings = [("!", "."), ("ä", "ae"), ("ö", "oe"), ("ü", "ue"),
                    ("ß", "ss")]

        for m in mappings:
            simplified = simplified.replace(m[0], m[1])

        return simplified

    def _create_cw_sequence(self, plain_text):
        cw_sequence = ""

        for t in plain_text:
            if t == " ":
                cw_sequence = cw_sequence + " "
                cw_sequence = cw_sequence + " "
                cw_sequence = cw_sequence + " "
            else:
                cw_sequence = cw_sequence + self._alphabet[t.lower()]
                cw_sequence = cw_sequence + " "
        return cw_sequence

    def _create_time_sequence(self, cw_sequence):
        duration_seconds = 0

        sequence = []

        for t in cw_sequence:
            if t == ".":
                up = duration_seconds
                duration_seconds = duration_seconds + self._dit_ms
                sequence.append((up, duration_seconds))
                duration_seconds = duration_seconds + self._dit_ms
            elif t == "-":
                up = duration_seconds
                duration_seconds = duration_seconds + self._dah_ms
                sequence.append((up, duration_seconds))
                duration_seconds = duration_seconds + self._dit_ms
            elif t == " ":
                duration_seconds = duration_seconds + self._dah_ms - self._dit_ms

        return sequence

    def _write_wav_file(self, file_name, sequence):
        duration_seconds = int(sequence[-1][1] + (2 * self._dah_ms))

        print("The CW text is " + str(duration_seconds) + " seconds long.")

        periods_per_second = 680
        samples_per_second = 8000
        samples_per_period = samples_per_second / periods_per_second
        amplification = 100

        with wave.open(file_name, "wb") as w:
            w.setnframes(samples_per_second * duration_seconds)
            w.setnchannels(1)
            w.setsampwidth(1)
            w.setframerate(samples_per_second)

            for n in range(samples_per_second * duration_seconds):
                angle = (n / samples_per_period) * 2 * math.pi
                time = n / samples_per_second
                value = amplification
                if len(sequence) > 0:
                    if time > sequence[0][0] and time < sequence[0][1]:
                        modulation = amplification

                        if time < sequence[0][0] + self._ramp_ms:
                            modulation = amplification * (
                                time - sequence[0][0]) / self._ramp_ms
                        if time > sequence[0][1] - self._ramp_ms:
                            modulation = amplification * (sequence[0][1] -
                                                          time) / self._ramp_ms

                        value = int(
                            math.sin(angle) * modulation) + amplification
                    if time >= sequence[0][1]:
                        sequence = sequence[1:]
                w.writeframes(struct.pack("B", value))

    def generate(self, text, file_name):
        text = self._simplyfy(text)
        cw_sequence = self._create_cw_sequence(text)
        signal_sequence = self._create_time_sequence(cw_sequence)
        self._write_wav_file(file_name, signal_sequence)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        exit()

    with open(sys.argv[1], "r") as textfile:
        text = (" ".join(textfile.readlines())).replace("\n", "=")

        cw_gen = CwGen()
        cw_gen.generate(text, sys.argv[2])

        winsound.PlaySound(sys.argv[2], winsound.SND_FILENAME)
