# Created by Terence Ho and Blake Bendock-Yang
# December 29th 2018
import json
from pprint import pprint

# parse through story_data


with open("story_data.json") as data_file:
	data = json.load(data_file)
	
	storyCollectionList = []

	storyCollectionCounter = 0;
	for i in range(len(data)):
		storyCollection = data["storyCollection"][storyCollectionCounter] # 0 = first section = "The Word"
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

		# print(initialrectList[0][0]) # example: statement prints out x1 value
		# storyCollectionList.append([storyCollectionCounter][initialrectList][finalrectList])
		storyCollectionCounter += 1;