from talon import imgui, Module, Context, actions, ui

 
import os

mod = Module()
mod.list("tutorials", desc="list of included talon tutorials")

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

tutorial_folder = os.path.join(__location__, "tutorials")
save_location_of_current_tutorial = os.path.join(__location__, "current_tutorial.txt")

current_future = os.path.join(__location__, 'future.txt')
current_present = os.path.join(__location__, 'present_line.txt')
current_past = os.path.join(__location__,'past.txt')


ctx = Context()

tutorial_names_list = os.listdir(tutorial_folder)

spoken_forms = [line.split(".")[1].lower() for line in tutorial_names_list]

tutorial_menu = dict(zip(spoken_forms, tutorial_names_list))

print(tutorial_names_list)

selected_tutorial = None

ctx.lists["self.tutorials"] = tutorial_menu

print(ctx.lists["self.tutorials"])

@imgui.open(y=0)
def list_tutorials(gui: imgui.GUI): 
	global future_ten_lines
	gui.text("Tutorials")
	gui.line()
	#[f for f in listdir(mypath) if isfile(join(mypath, f))]
	text = [f for f in os.listdir(tutorial_folder) if os.path.isfile(os.path.join(tutorial_folder,f))] 
	for line in text:
		tutorial_name = line.split(".")
		tutorial_number = tutorial_name[0]
		basename = tutorial_name[1]
		if gui.button(basename):
			selected_tutorial = basename
			list_tutorials.hide()

			## Load tutuorial from it's previous state.  It's previous sta 
			if os.path.isdir( tutorial_folder + '\\' + tutorial_number + '.' + basename):
				print('directory exists')
			else:
				print('directory does not exist')

				initialize_tutorial_files(tutorial_folder, tutorial_number, basename)


			# Check what currently open file is.  
			save_current_tutorial()
			open_selected_tutorial(tutorial_folder, tutorial_number, basename)

			actions.user.launch_current_tutorial()
	gui.line()
	gui.text("tutorial close")


def initialize_tutorial_files(tutorial_folder, tutorial_number, basename):
	print('did I get called, I am initialized')

	tutorial_name = tutorial_number + '.' + basename
	name_with_extension = tutorial_name + ".md"

					# create file 
	os.mkdir(tutorial_folder + '\\' + tutorial_name)    			
	with open (tutorial_folder + '\\' + name_with_extension , 'r') as read_original_tutorial:
		past_lines = read_original_tutorial.read().splitlines(True)
		past_lines = [ x for x in past_lines if x.strip()]  ## uneligant way to get rid of all the blank lines in the markdown file so that I'm not stuck saying 'next line' on blank lines 
		read_original_tutorial.close()

	### copy tutorial into past out file
	with open (tutorial_folder + '\\'  + tutorial_name + "\\" + name_with_extension + ".future",'w') as to_be_read:
		to_be_read.writelines(past_lines)
		to_be_read.close()

	### save blank present file
	with open (tutorial_folder + '\\'  + tutorial_name + "\\" + name_with_extension + ".present_line",'w') as currently_reading:
		currently_reading.close()

	### save blank future file
	with open (tutorial_folder + '\\'  + tutorial_name + "\\" + name_with_extension + ".past",'w') as already_read:
		already_read.close()

def save_current_tutorial():

	if os.path.isfile(save_location_of_current_tutorial):
	#save current state back to tutorials before overwriting it with the new thing
		with open (save_location_of_current_tutorial,'r') as current_tut_in:
			file_to_be_saved = current_tut_in.read().splitlines(True)[0]
			current_tut_in.close()

			save_path = file_to_be_saved.split(".md")[0]
			save_basename = file_to_be_saved.split("\\")[-1]
			
			# Open future.txt and read it

			with open (current_future, 'r') as futurein:
				future_lines = futurein.read().splitlines(True)
				futurein.close()

			# Open the tutorial file and write it. 
			with open (save_path +"\\" + save_basename + ".future",'w') as futureout:
				futureout.writelines(future_lines)
				futureout.close()


			# open past.txt and read it

			with open (current_past,'r') as pastin:
				past_lines = pastin.read().splitlines(True)
				pastin.close()


			# open tutorial file and write it
			with open (save_path +"\\" + save_basename + ".past",'w') as pastout:
				pastout.writelines(past_lines)
				pastout.close()

			with open (current_present,'r') as current_line_in:
				current_line = current_line_in.read().splitlines(True)
				current_line_in.close()


			# open tutorial file and write it
			with open (save_path +"\\" + save_basename + ".present_line",'w') as current_line_out:
				current_line_out.writelines(current_line)
				current_line_out.close()

def open_selected_tutorial(tutorial_folder, tutorial_number,  basename):
	with open (save_location_of_current_tutorial,'w') as current_tut_out:
			current_tut_out.writelines( tutorial_folder + "\\" + tutorial_number + "." + basename + ".md" )
			current_tut_out.close()

	### copy the files to their working locations.  
	### copy future reading to future file  			
	with open (tutorial_folder + "\\" + tutorial_number + '.' + basename + "\\" + tutorial_number + "." + basename + ".md"  + ".future",'r') as futurein:
			future_lines = futurein.read().splitlines(True)
			futurein.close()

	with open (current_future,'w') as futureout:
			futureout.writelines(future_lines)
			futureout.close()

	### copy present line to present file  			
	with open (tutorial_folder + "\\" +  tutorial_number + '.' + basename + "\\" + tutorial_number + "." + basename + ".md" + ".present_line",'r') as futurein:
			future_lines = futurein.read().splitlines(True)
			futurein.close()

	with open (current_present,'w') as futureout:
			futureout.writelines(future_lines)
			futureout.close() 		

	### copy past line to past file
	with open (tutorial_folder + "\\" + tutorial_number + '.' + basename + "\\" + tutorial_number + "." + basename + ".md"  + ".past",'r') as futurein:
			future_lines = futurein.read().splitlines(True)
			futurein.close()

	with open (current_past,'w') as futureout:
			futureout.writelines(future_lines)
			futureout.close() 




def tutorial_launcher(filename:str =""): 
	actions.user.tutorial_draft_hide()
	
	with open (current_present,'r') as current_line_in:
		current_line = current_line_in.read().splitlines(True)
		current_line_in.close()

	if len(current_line) == 0:
		actions.user.tutorial_draft_show("Say 'Next Line to go to the next line.  Say 'last line' to go to the last line.")
	else:
		actions.user.tutorial_draft_show(current_line[0])
	actions.user.tutorial_draft_resize(ui.main_screen().width*1/2, ui.main_screen().height*1/3) #ui.main_screen().height*2/3
	actions.user.tutorial_draft_named_move('left')
	#actions.user.show_future()
	#actions.user.show_past()


@mod.action_class
class Actions:
	def show_tutorial_list(): 
		"""Show list of introductory tutorials"""
		list_tutorials.show()

	def hide_tutorial_list():
		"""hide list of introductory tutorials"""
		list_tutorials.hide()

	def tutorial_select_by_name(file_name:str):
		"""select by name""" 
		if list_tutorials.showing:
			list_tutorials.hide()
			#when I say something from the context list 'tutorials'
			#   it makes the tutorial list disappear"
			print("i am printing" + file_name)
			#tutorial_launcher()

		tutorial_name = file_name.split(".")
		tutorial_number = tutorial_name[0]
		basename = tutorial_name[1]

		if os.path.isdir( tutorial_folder + '\\' + tutorial_number + '.' + basename):
			print('directory exists')
		else:
			print('directory does not exist')
			initialize_tutorial_files(tutorial_folder, tutorial_number, basename)


		# Check what currently open file is.  
		save_current_tutorial()
		open_selected_tutorial(tutorial_folder, tutorial_number, basename)

		actions.user.launch_current_tutorial()


	def launch_current_tutorial():
		"""launch current tutorial"""
		tutorial_launcher()


	def save_current_tutorial():
		"""save current tutorial"""
		save_current_tutorial()




