import audiolab, scipy
a, fs, enc = audiolab.wavread('file1.wav')
b, fs, enc = audiolab.wavread('file2.wav')
c = scipy.vstack((a,b))
audiolab.wavwrite(c, 'file3.wav', fs, enc)

# ------------------- РАБОТАЕТ!

import wave
infiles = ["2.wav", "sad_new_year.wav"]
outfile = "2021.wav"
data = []
for infile in infiles:
    w = wave.open(infile, 'rb')
    data.append( [w.getparams(), w.readframes(w.getnframes())] )
    w.close()

output = wave.open(outfile, 'wb')
output.setparams(data[0][0])
output.writeframes(data[0][1])
output.writeframes(data[1][1])
output.close()

# -------------------

from pydub import AudioSegment

sound1 = AudioSegment.from_wav("/path/to/file1.wav")
sound2 = AudioSegment.from_wav("/path/to/file2.wav")

combined_sounds = sound1 + sound2
combined_sounds.export("/output/path.wav", format="wav")