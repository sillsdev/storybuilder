import json
import re

input_src = "story_data.json"
output_src = "story_data_proc.json"

input_raw = ""
with open(input_src) as file:
	input_raw = file.read()
	file.close()

#remove hanging commas (breaks json lib)

input_raw = re.sub(r",(\s+)\}",r"\1}",input_raw)
input_raw = re.sub(r",(\s+)\]",r"\1]",input_raw)

data = json.loads(input_raw)

def process(pages):
	result = []
	for i in range(len(pages)):
		page = pages[i]
		page["ref_start"] = re.sub(r"[a-z]",'',page["ref_start"])
		page["ref_end"] = re.sub(r"[a-z]",'',page["ref_end"])
		if len(result) == 0 or result[-1]["ref_end"] != page["ref_start"]:
			result.append(page)
		else:
			result[-1]["ref_end"] = page["ref_end"]
	for i in range(len(result)):
		result[i]["page"] = i + 1
	return result

for i in range(len(data["storyCollection"])):
	data["storyCollection"][i]["story"]["pages"] = process(data["storyCollection"][i]["story"]["pages"])

# just some formatting for outut json
def flatten(match):
    result = match.group(0)
    result = re.sub(r",\s+", ', ', result)
    result = re.sub(r"\s+\}", ' }', result)
    result = re.sub(r"\{\s+", '{ ', result)
    return result

output = json.dumps(data,indent=4, sort_keys=False)
output = re.sub(r"\{[^\[\]\{\}]+\}",flatten,output)

with open(output_src,"w+") as file:
	file.write(output)
