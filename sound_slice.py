from pydub import AudioSegment
import json
import re

timing_src = [ 
  "./inputs/timing/04-JHN-01-timing.txt",
  "./inputs/timing/04-JHN-02-timing.txt",
  "./inputs/timing/04-JHN-03-timing.txt",
  "./inputs/timing/04-JHN-04-timing.txt",
  "./inputs/timing/04-JHN-05-timing.txt",
  "./inputs/timing/04-JHN-06-timing.txt",
  "./inputs/timing/04-JHN-07-timing.txt",
  "./inputs/timing/04-JHN-08-timing.txt",
  "./inputs/timing/04-JHN-09-timing.txt",
  "./inputs/timing/04-JHN-10-timing.txt",
  "./inputs/timing/04-JHN-11-timing.txt",
  "./inputs/timing/04-JHN-12-timing.txt",
  "./inputs/timing/04-JHN-13-timing.txt",
  "./inputs/timing/04-JHN-14-timing.txt",
  "./inputs/timing/04-JHN-15-timing.txt",
  "./inputs/timing/04-JHN-16-timing.txt",
  "./inputs/timing/04-JHN-17-timing.txt",
  "./inputs/timing/04-JHN-18-timing.txt",
  "./inputs/timing/04-JHN-19-timing.txt",
  "./inputs/timing/04-JHN-20-timing.txt",
  "./inputs/timing/04-JHN-21-timing.txt"
]

audio_src = [ 
  "./inputs/mp3/44-JHNgul-01.mp3",
  "./inputs/mp3/44-JHNgul-02.mp3",
  "./inputs/mp3/44-JHNgul-03.mp3",
  "./inputs/mp3/44-JHNgul-04.mp3",
  "./inputs/mp3/44-JHNgul-05.mp3",
  "./inputs/mp3/44-JHNgul-06.mp3",
  "./inputs/mp3/44-JHNgul-07.mp3",
  "./inputs/mp3/44-JHNgul-08.mp3",
  "./inputs/mp3/44-JHNgul-09.mp3",
  "./inputs/mp3/44-JHNgul-10.mp3",
  "./inputs/mp3/44-JHNgul-11.mp3",
  "./inputs/mp3/44-JHNgul-12.mp3",
  "./inputs/mp3/44-JHNgul-13.mp3",
  "./inputs/mp3/44-JHNgul-14.mp3",
  "./inputs/mp3/44-JHNgul-15.mp3",
  "./inputs/mp3/44-JHNgul-16.mp3",
  "./inputs/mp3/44-JHNgul-17.mp3",
  "./inputs/mp3/44-JHNgul-18.mp3",
  "./inputs/mp3/44-JHNgul-19.mp3",
  "./inputs/mp3/44-JHNgul-20.mp3",
  "./inputs/mp3/44-JHNgul-21.mp3"
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
  raw = raw.strip()
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
      curr_start = x[0]
    curr_end = x[1]

  timings2.append((curr_start,curr_end,curr_verse))
  timings = timings2[1:]

  for t in timings:
    #print(t)
    start = t[0]
    end = t[1]
    seg = audio[i][start:end]
    segments[i].append(seg)

  #print(timings)

stories = json.loads(pages_raw)

# assumes that start and end are in the same book
def get_seg(ref_start,ref_end):
  seg = AudioSegment.empty()
  m_start = re.match(r"([0-9]+):([0-9]+)",ref_start)
  m_end = re.match(r"([0-9]+):([0-9]+)",ref_end)
  book = int(m_start.group(1))
  verse_start = int(m_start.group(2))
  verse_end = int(m_end.group(2))
  #print(book,verse_start,verse_end)
  for verse in range(verse_start,verse_end+1):
    seg += segments[book-1][verse-1]
  return seg

def format_book_title(t):
  return re.sub(r"[ -]",'_',t)

# produce audio files for a story
def segment_story(story):
  durations = [] # in millis
  filenames = []
  for p in story["pages"]:
      seg = get_seg(p["ref_start"],p["ref_end"])
      filename = "./outputs/{0}_{1:02d}.mp3".format(format_book_title(story["title"]),p["page"])
      file = open(filename,"w+")
      file.write(' ')
      file.close()
      seg.export(filename, format="mp3")
      print(filename)
      durations.append(len(seg))
      filenames.apppend(filename)
  return filenames, durations

if __name__ == "__main__":
  for story in stories["storyCollection"]:
    segment_story(story["story"])

# print by verse
'''
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
