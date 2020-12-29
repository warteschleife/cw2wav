import wave, math, random, winsound, struct, sys, re


def get_morse_table(file_name):
    result = {}
    with open("alphabet.txt", "r") as morse_table:
        for line in morse_table.readlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue
            elements = re.match("^(\\S)\\s+([\\.-]+)$", line)
            if elements:
                if elements.group(1) in result.keys():
                    raise Exception("Duplicate definition for character '" +
                                    elements.group(1) + "'")
                result[elements.group(1)] = elements.group(2)
            else:
                raise Exception("Invalid line in '" + file_name + "': \"" +
                                line + "\"")
    return result


class CwGen:
    def __init__(self, alphabet, sampling_rate=44000, len_dit=0.1):
        len_dit = len_dit
        len_dah = 3 * len_dit
        ramp_time = len_dit / 8

        self._sampling_rate = sampling_rate
        self._tone_dit = self._generate_tone(len_dit, 100, ramp_time)
        self._tone_dah = self._generate_tone(len_dah, 100, ramp_time * 3)
        self._separate_tone = self._generate_tone(len_dit, 0, 0)
        self._separate_char = self._generate_tone(len_dah, 0, 0)

        self._alphabet = alphabet

    def _generate_tone(self, duration, volume, ramp_time):
        samples = bytearray()

        periods_per_second = 680

        samples_per_period = self._sampling_rate / periods_per_second

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


if __name__ == "__main__":
    if len(sys.argv) < 3:
        exit()

    try:
        alphabet = get_morse_table("alphabet.txt")
    except Exception as ex:
        print(ex)
        exit(-1)

    with open(sys.argv[1], "r") as textfile:
        text = "vvv  " + (" ".join(textfile.readlines())).replace("\n", "=")

        cw_gen = CwGen(alphabet, len_dit=0.12)

        try:
            cw_gen.generate(text, sys.argv[2])
        except Exception as ex:
            print(ex)
            exit(-1)

        winsound.PlaySound(sys.argv[2], winsound.SND_FILENAME)
