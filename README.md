# storybuilder
Story builder for Urbana #Hack4Missions

## Dependencies:
	Install Python

	Pydub and FFmpeg
		https://github.com/jiaaro/pydub#installation
			Download and extract FFmpeg from binaries at https://ffmpeg.zeranoe.com/builds/
			Add the path to the /bin folder to your PATH environment variable

		Install Pydub
			pip install pydub
			https://pypi.org/project/pydub/


## Troubleshooting notes:
	audio_slice/slice.py notes:
		Warn() about lack of FFMPEG
			Make sure to install FFmpeg
		Runtime error about can't parse string with ? and other funny characters at the beginning
			Remove the byte order marker at the beginning. You can probably just copy and paste the text into a new notepad instance and save.
		Runtime error about can't parse string, blank error:
			Probably a problem with Mac vs. WIndows line endings. Convert the line endings or save them into a new notepad instance. Or fix the code to make it more robust.

## Follow-ups
[v2 branch](https://github.com/sillsdev/storybuilder/tree/v2): Additional improvements made by Bruce after the hackathon, and some compatability fixes.
https://github.com/sillsdev/appbuilder-storybuilder: Follow-up version in Go to integrate the project into App Builder, which is the most recent work as of 2023.
