

tutorial menu: 
	user.show_tutorial_list()
	mode.enable("user.help")

# These commands are going to cause problems later on if I don't throw a mode on them when the window is actually open. 

hide tutorial list: 
	user.hide_tutorial_list()
	mode.disable("user.help")
