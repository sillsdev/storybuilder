from pydub import AudioSegment
import json
import re

timing_src = [ 
	"./inputs/04-JHN-01-timing.txt",
	"./inputs/04-JHN-02-timing.txt",
	"./inputs/04-JHN-03-timing.txt"
]

audio_src = [ 
	"./inputs/44-JHNgul-01.mp3",
	"./inputs/44-JHNgul-02.mp3",
	"./inputs/44-JHNgul-03.mp3"
]

pages_src = "./inputs/story_data.json"

timing_raw = []
pages_raw = ""
audio = []

for t in timing_src:
	with open(t) as file:
		timing_raw.append(file.read())

for a in audio_src:
	audio.append(AudioSegment.from_mp3(a))

with open(pages_src) as file:
	pages_raw = file.read()

segments = []
for i in range(len(timing_raw)):
	segments.append([])
	raw = timing_raw[i]
	raw = raw.replace('\ufeff','')
	timings = raw.split("\n")
	timings = [x.split("\t") for x in timings]
	timings = [(float(x[0]), float(x[1]), x[2]) for x in timings]
	timings = [(int(x[0] * 1000), int(x[1] * 1000), x[2]) for x in timings]
	timings = [x for x in timings if x[2][0].isdigit()]

	#print(timings)
	timings2 = []

	curr_verse = 0
	curr_start = 0
	curr_end = 0
	for x in timings:
		verse = int(re.match(r"[0-9]+",x[2]).group(0))
		if verse != curr_verse:
			timings2.append((curr_start,curr_end,curr_verse))
			curr_verse = verse
			curr_start = int(x[0])
		curr_end = int(x[1])

	timings2.append((curr_start,curr_end,curr_verse))
	timings = timings2[1:]

	for t in timings:
		#print(t)
		start = t[0]
		end = t[1]
		seg = audio[i][start:end]
		segments[i].append(seg)

	#print(timings)

#pages = json.loads(pages_raw)
#print(pages["storyCollection"][0]["story"])


for i in range(len(segments)):
	for j in range(len(segments[i])):
		#print(i,j)
		filename = "./outputs/{0:02d}_{1:02d}.mp3".format(i+1,j+1)
		file = open(filename,"w+")
		file.write(' ')
		file.close()
		segments[i][j].export(filename, format="mp3")
		print(filename)


'''
for t in timings:
	filename = "./outputs/{0:02d}.mp3".format(t[2])
	file = open(filename,"w+")
	file.write(' ')
	file.close()
	my_slice = audio[t[0]:t[1]]
	my_slice.export(filename, format="mp3")
'''