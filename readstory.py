# -*- coding: utf-8 -*-

import json
from pprint import pprint

# parse through story_data

with open("story_data.json") as data_file:
	d = json.load(data_file)
	# print d

	for index in range(len(d)):
		storyCollection = d["storyCollection"][0]
		# pprint(storyCollection)
		for index in range(len(storyCollection)):
			story = storyCollection["story"]
			# pprint(story)
			for index in range(len(story)):
				pages = story["pages"]
				pprint(pages)
				# for index in range(len(pages)):
					# spilt string

		# print [for pages in storyCollection if(d["page"] == 1)] 

	# for d["page"] in d["pages"]
    	# initalrectArray.append = d["pages"]["page"][x]["img_initialrect"]
    		
 #    	finalrectArray.append = data["pages"]["page"][x]["img_finalrect"]
    	
