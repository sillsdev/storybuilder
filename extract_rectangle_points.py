# extract_rectangle_points
# parse through story_data
# Created by Terence Ho and Blake Bendock-Yang
# December 29th 2018

import json
from pprint import pprint

def parse_data(storyCollection):
  storyCollectionList = []
  initialrectList = []
  finalrectList = []

  output = []

   # pprint(storyCollection)
  for i in range(len(storyCollection)):
    story = storyCollection["story"]
    # pprint(story)
    for i in range(len(story)):
      pages = story["pages"]
    
    index = 0
    initialrectList = []
    finalrectList = []
    for i in range(len(pages)):
      # print(pages[index]["img_initialrect"].split(" "))

      initialrectList.append(pages[index]["img_initialrect"].split(" "))
      finalrectList.append(pages[index]["img_finalrect"].split(" "))

      # print("img_initialrect:       " + pages[index]["img_initialrect"])
      # print("img_finalrect:         " + pages[index]["img_finalrect"])
      index += 1;

    # Shows entire list
    # print(initialrectList)
    # print(finalrectList)

  # calculate zoom values and add to list
  counter = 0;
  zoomValue = 0.00;
  for i in range(len(initialrectList)):
    zoomValue = float(1)/float(initialrectList[counter][3])
    initialrectList[counter].remove(initialrectList[counter][3])
    initialrectList[counter].remove(initialrectList[counter][2])
    initialrectList[counter].append(zoomValue)

    zoomValue = float(1)/float(finalrectList[counter][3])
    finalrectList[counter].remove(finalrectList[counter][3])
    finalrectList[counter].remove(finalrectList[counter][2])
    finalrectList[counter].append(zoomValue)

    output.append(tuple(initialrectList[counter] + finalrectList[counter]))

    counter += 1

  # print(initialrectList[0][0]) # example: statement prints out x1 value [page#][x or y or z]

  # storyCollectionList.append([storyCollectionCounter][initialrectList][finalrectList])

  return output
