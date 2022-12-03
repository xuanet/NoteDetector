import audio2numpy as a2n
import numpy as np
import math
import matplotlib
import sounddevice as sd
import soundfile as sf
import scipy.io.wavfile as wav
import scipy.signal as signal
import matplotlib.pyplot as plt

FS = 44100
amp = 2 * np.sqrt(2)
thresh = 0.5

#sample_rate, samples = wav.read(filename)

x,fs=a2n.audio_from_file("Ekemini.mp3")
x_combined = [i[0] + i[1] for i in x]

f, t, Zxx = signal.stft(x_combined, fs=FS, nperseg = 8000, nfft = 10000)

Zxx = np.abs(Zxx)
def topFour(array, frequencies):
    output = []
    if len(array) <= 4:
        for element in array:
            output.append(frequencies[element[1]])
        return sorted(output)
    sortedArray = sorted(array)
    reducedArray = sortedArray[-4:]
    for element in reducedArray:
        output.append(frequencies[element[1]])
    return sorted(output)


def findNotes(t, f, Zxx, thresh):
    score = [0] * len(t)
    for time in range(len(t)):
        score[time] = [t[time]]
        notes = Zxx[time]
        activeNotes = []
        for freq in range(len(notes)):
            if notes[freq] >= thresh:
                activeNotes.append([notes[freq], freq])

        notesDetected = topFour(activeNotes, f)
        score[time].append(notesDetected)
    return score


thresh = 0.1

Zxx_transpose = [list(i) for i in zip(*Zxx)]

music = findNotes(t, f, Zxx_transpose, thresh)

s = "In the list of lists printed below, the first element of each list is the time in seconds, and the second element is the list of frequencies occurring at this time."

print(s + "\n")

print(music)

y = [element[1] for element in music]
x = [element[0] for element in music]

for xe, ye in zip(x, y):
    plt.scatter([xe] * len(ye), ye, color='r')

plt.title("Ekemini's Song")
plt.xlabel("Time (s)")
plt.ylabel("Note Pitch (Hz)")

my_set = set({})
for i in y:
    for j in i:
        my_set.add(j)

print("Distinct frequencies used: " + str(sorted(my_set)))