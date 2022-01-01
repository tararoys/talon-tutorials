mode: command
mode: dictation
-

^tutorial open:
	#Shows a single-sentence draft composition widow, the future ten things that window needs to interact with, and the last ten things that window wrote. Think of it like a mad-libs scroll. 
	user.launch_current_tutorial()
	mode.enable("user.help")




