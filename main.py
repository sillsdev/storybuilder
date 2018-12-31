#!/usr/bin/env python3
import json
from subprocess import call
from os.path import sep

import split_text, extract_rectangle_points, sound_slice

def assemble_page(soundfile, duration, image, motion, outfile):

  #startx, starty, startz, endx, endy, endz = motion
  #zoompan = f"zoompan=x='{startx}*iw+({endx}-{startx})/zoom':y='{starty}+({endy}-{starty})/zoom':z='if(eq(on,1),{startz},zoom+({endz}-{startz})/(25*{duration}))':d='25*{duration}':s=1600*900"
  zoompan = "zoompan=x='{1}*iw+({4}-{1})/zoom':y='{2}+({5}-{2})/zoom':z='if(eq(on,1),{3},zoom+({6}-{3})/(25*{0}))':d='25*{0}':s=1600*900".format(duration, *motion)
  call(["ffmpeg", "-i", "inputs"+sep+"images"+sep+image, "-i", soundfile, "-filter_complex", zoompan, outfile])
  #call(["ffmpeg", "-i", "inputs"+sep+"images"+sep+image, "-i", soundfile, outfile])

def stitch_pages(pages_filename, title, length):
  call(["ffmpeg", "-f", "concat", "-safe", "0", "-i", pages_filename, "-c", "copy", "outputs"+sep+title+".flv"])

def get_image_list(story):
  return [page["img_src"] for page in story["pages"]]

if __name__ == "__main__":

    with open("inputs/story_data.json", "r") as json_file, open(
        "john.sfm", "r", encoding='utf_8'
    ) as john:
        story_collection = json.load(json_file)
        book_of_john = split_text.gen_book(john)
        for story in story_collection["storyCollection"]:
          #strings = split_text.split_texts(story["story"], book_of_john)
          motions = extract_rectangle_points.parse_data(story)
          soundfiles, durations = sound_slice.segment_story(story["story"])
          images = get_image_list(story["story"])
          assert( len(soundfiles) == len(motions) == len(durations) == len(images) )

          title = story["story"]["title"].replace("'","")

          pages_filename = "outputs"+sep+title+".pages.txt"
          with open(pages_filename, "w") as pagesfile:
            for i in range(len(images)):
              filename = "outputs"+sep+title+str(i)+".flv"
              assemble_page(soundfiles[i], durations[i], images[i], motions[i], filename)
              pagesfile.write("file '"+filename+"'\n")

          stitch_pages(pages_filename, title, len(images))