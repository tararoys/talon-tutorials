mode: user.help

-

tutorial close:
	# hides the whole little app.
	user.save_current_tutorial() 
	user.tutorial_draft_hide()
	user.hide_future()
	user.hide_past()
	user.hide_tutorial_list()
	mode.disable("user.help")

next line:
	user.write_next_step()

last line: 
	user.write_last_step()

show future: 
	user.show_future()

hide future:
	user.hide_future()

show past:
	user.show_past()

hide past:
	user.hide_past()

line view: 
	user.hide_past()
	user.hide_future()

page view: 
	user.show_past()
	user.show_future()