#!/usr/bin/env python3
import json
import split_text as st

if __name__ == "__main__":

    with open("../audio_slice/inputs/story_data.json", "r") as json_file, open(
        "john.sfm", "r"
    ) as john:
        story_collection = json.load(json_file)
        book_of_john = st.gen_book(john)
        for story in story_collection["storyCollection"]:
            # beginnings of a proper test situation
            print(len(st.split_texts(story["story"], book_of_john)))
