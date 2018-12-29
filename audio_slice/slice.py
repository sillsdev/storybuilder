from pydub import AudioSegment

timing_src = "./inputs/04-JHN-01-timing.txt"
audio_src = "./inputs/44-JHNgul-01.mp3"

timing_raw = ""
audio = AudioSegment.from_mp3(audio_src)

with open(timing_src) as file:
	timing_raw = file.read()

timing_raw = timing_raw.replace('\ufeff','')
timings = timing_raw.split("\n")
timings = [x.split("\t") for x in timings]
timings = [(float(x[0]), float(x[1]), x[2]) for x in timings]
timings = [(int(x[0] * 1000), int(x[1] * 1000), x[2]) for x in timings]

i = 0
for t in timings:
	filename = "./outputs/{0:03d}_{1}.mp3".format(i,t[2])
	i += 1
	file = open(filename,"w+")
	file.write(' ')
	file.close()
	my_slice = audio[t[0]:t[1]]
	my_slice.export(filename, format="mp3")