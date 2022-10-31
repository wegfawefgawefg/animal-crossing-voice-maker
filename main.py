import os
from pprint import pprint

from playsound import playsound
from scipy.io import wavfile
from scipy.io.wavfile import write
import numpy as np

voice_path = "voices/guy3"
files = os.listdir(voice_path)
files.sort()
sounds = {}
for file in files:
    raw_name = file.split(".")[0]
    fp = os.path.join(voice_path, file)
    rate, data = wavfile.read(fp)

    channel_one = data[:, 0]
    sounds[raw_name] = channel_one
pprint(sounds)

sample_rate = 48000
speed_multiplier = 1.7
advance = 0.15 * sample_rate
space_skip = 0.4 * advance

say_this = "This is a test of the animal crossing style talking machine"
say_this = "mestr lokee i mess yu bro"
say_this = "pastee luuk at des"
say_this = "kil haw es yor de goeng"
say_this = "weleam haw was yor de"
say_this = "i med somteng kul"
say_this = "ame  i lov yuu vere alat"
say_this = "ef yu wurk hard yu wel hav a gud lif"
say = say_this.lower().strip()
cursor = 0
notes = []
for char in say:
    notes.append((char, cursor))
    if char == " ":
        cursor += space_skip
    else:
        cursor += advance
# advance the cursor by the length of the last note
last_char = say[-1]
last_note = sounds[last_char]
last_note_length = last_note.shape[0]
cursor += last_note_length

end_pad = sample_rate * 1.0
buffer_length = int(cursor + end_pad)
base = np.zeros(buffer_length, dtype=np.int16)

for note in notes:
    char = note[0]
    cursor = note[1]
    if char not in sounds:
        continue
    sound = sounds[char]
    start = int(cursor)
    end = int(start + sound.shape[0])
    print(f"Adding {char} from {start} to {end}")
    selection = base[start:end]
    print(selection.shape)
    print(sound.shape)
    base[start:end] += sound

output_dir = "output"
if not os.path.exists(output_dir):
        os.makedirs(output_dir)

name = say_this.replace(" ", "_")
file_path = os.path.join(output_dir, name + '.wav')
write_rate = int(sample_rate*speed_multiplier)
write(file_path, write_rate, base.astype(np.int16))
playsound(file_path)
# for file in files:
#     playsound(voice_path + "/" + file)

