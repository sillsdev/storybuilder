#!/usr/bin/env python3
import json
from subprocess import call

import split_text, extract_motion, sound_slice

def assemble_page(soundfile, duration, text, image, motion, outfile):
  
  startx = motion["x0"]
  starty = motion["y0"]
  startz = motion["z0"]
  endx = motion["x1"]
  endy = motion["y1"]
  endz = motion["z1"]

  zoompan = f"zoompan=x='{startx}+({endx}-{startx})/zoom':y='{starty}+({endy}-{starty})/zoom':z='if(eq(on,1),{startz},zoom+({endz}-{startz})/(25*{duration}))':d='25*{duration}':s=1600*900"
  call(["ffmpeg", "-i", image, "-i", soundfile, "-filter_complex", zoompan, outfile])

def stitch_pages(pages_filename, title, length):
  call(["ffmpeg", "-f", "concat", "-i", pages_filename, "-c", "copy", "outputs/"+title+".flv"])

if __name__ == "__main__":

    with open("story_data.json", "r") as json_file, open(
        "john.sfm", "r"
    ) as john:
        story_collection = json.load(json_file)
        book_of_john = split_text.gen_book(john)
        for story in story_collection["storyCollection"]:
          strings = split_text.split_texts(story["story"], book_of_john)
          motions = extract_motion.extract(story)
          soundfiles, durations = sound_slice.segment_story(story["story"])
          images = get_image_list()
          assert( len(strings) == len(motions) == len(durations) == len(images) )
          pages_filename = "outputs/"+story["title"]+".pages.txt"
          with open(pages_filename, "w") as pagesfile:
            for i in len(strings):
              filename = "outputs/"+story["title"]+str(i)+".flv"
              assemble_page(soundfiles[i], durations[i], strings[i], images[i], motions[i], )
              pagesfile.write("file '"+filename+"'")

          stitch_pages(pages_filename, story["title"], len(strings))