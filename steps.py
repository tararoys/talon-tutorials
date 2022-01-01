
from talon import Module, Context, actions, imgui, ui
import re, os
mod = Module()
ctx = Context()

mod.mode("tutorial", "mode for commands that are available only when tutorial windows like the tutorial window and the tutorial selection menu are visible")

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# The UI for this tutorial is as follows
# | window showing past 10 lines |
# |______________________________|
#   | editable draft window     |
#   | showing exactly one       |
#   | sentence's worth of       |
#   | editable text             |
# |------------------------------|
# | next ten lines in the future |
# |
#
# This is the same visual idea of a book or a document in a modern word processor, but stripped down 
# and very tightly focused.  By 
# 1. allowing stepping through a tutorial sentence by sentence,    
# 2. only allowing one sentence to be edited at a time
# removes all distraction from the learning process.  
#
# This is an interactive, computer version of reading a textbook with a ruler to keep
# of what ine you are on.  

# implimentation details:
#    I think of the above as a sheet of paper from a book cut in half with scissors. 
#    THe top is what I have already read. 
#    The middle is what I am reading 
#    the bottom paper is what I am going to read in the future.  
#      
#
#    When I finish reading the sentence in the current box, I need to: 
#       - *append* what I am currently reading to the *bottom* of the past file.
#       - delete what I was currently reading from the midddle draft box
#       - take the first line off the top of the future file and put it in the currently reading box
#
#  Note: appending things to files is easy, taking the first line off the file is not.     


past_ten_lines = [] # lines just read.  
future_ten_lines = [] #lines about to be read

present_line = "" # line I am currently reading

latest_line = ""

@imgui.open(x=0,y=ui.main_screen().height*2/3)
def future(gui: imgui.GUI):
    global future_ten_lines

    if len(future_ten_lines)> 0:
    	gui.text("NEXT LINE: " + future_ten_lines[0].strip())
    else: 
    	gui.text("Next Line: ")
    gui.line()
    text = future_ten_lines[1:]
    for line in text:
        gui.text(line.strip())

@imgui.open(x=0,y=0)
def past(gui: imgui.GUI): 
    global past_ten_lines
    text = past_ten_lines[0:9]
    for line in text:
        gui.text(line.strip())
    gui.line()
    if len(past_ten_lines) > 0:
    	gui.text("LAST LINE: " + past_ten_lines[-1].strip())
    else:
    	gui.text("LAST LINE:")


@mod.action_class
class Actions:
	def read_top_line():
		"""read first line of a file"""
		print("------------")
		print("\n")
		#with open(os.path.join(__location__, 'ok.txt', "r") as f:		
		#f.close()


		with open(os.path.join(__location__, 'future.txt'), 'r') as fin:
			data = fin.read().splitlines(True)
			future_ten_lines = data
			current_step = data[0]
			actions.user.tutorial_draft_show(current_step)
			print(current_step)

			fin.close()

	def write_last_step():
		"""move backwards one line in the tutorial"""

		# The write_last_step command is the command that is *supposed* to do all the following logid 
		#
		# 
		#
		# implimentation details:
		#    I think of the above as a sheet of paper from a book cut in half with scissors. 
		#    THe top is what I have already read. 
		#    The middle is what I am reading 
		#    the bottom paper is what I am going to read in the future. 
		#
		#	When I want to revisit a step, I say, 'last step'
		#         - I put the line I am currently working on at the top of the future document
		#         - write the last line from the past document to my middle draft box
		#         - delete the last line from the past document.  

		global past_ten_lines
		global present_line
		global future_ten_lines

		text_in_window =  actions.user.tutorial_draft_get_text() 

		if( text_in_window.strip() != False or text_in_window != "Say 'next line' to go to the next line.  Say 'last line' to go to the last line." ):
			present_line = text_in_window


		with open(os.path.join(__location__, 'future.txt'), 'r') as fin:
			future_data = fin.read().splitlines(True)
			fin.close()

		with open(os.path.join(__location__, 'future.txt'), 'w') as fout:
			fout.writelines(present_line)
			fout.writelines(future_data)
			fout.close()

		with open(os.path.join(__location__, 'future.txt'), 'r') as fin:
			future_data = fin.read().splitlines(True)
			future_ten_lines = future_data[:10]
			fin.close()


		with open (os.path.join(__location__, 'past.txt'),'r') as pastin:
			past_lines = pastin.read().splitlines(True)
			present_line = past_lines[-1]
			actions.user.tutorial_draft_show(present_line)
			pastin.close()
	
		with open (os.path.join(__location__, 'past.txt'),'w') as pastout:
			truncated_past_lines = past_lines[:-1]
			pastout.writelines(truncated_past_lines)
			pastout.close()

		with open (os.path.join(__location__, 'past.txt'),'r') as pastin:
			past_lines = pastin.read().splitlines(True)
			past_ten_lines = past_lines[-10:] 
			pastin.close()


	def write_next_step():
		"""Move forward one line in the tutorial."""

		# The write_next_step command is the command that is *supposed* to do all the following logid 
		#
		# 
		#
		# implimentation details:
		#    I think of the above as a sheet of paper from a book cut in half with scissors. 
		#    THe top is what I have already read. 
		#    The middle is what I am reading 
		#    the bottom paper is what I am going to read in the future.  
		#      
		#
		#    When I finish reading the sentence in the current box, I need to: 
		#       - *append* what I am currently reading to the *bottom* of the past file.
		#       - delete what I was currently reading from the midddle draft box
		#       - take the first line off the top of the future file and put it in the currently reading box
		#
		#  Note: appending things to files is easy, taking the first line off the file is not. 

		global past_ten_lines
		global present_line
		global future_ten_lines
		
		#save the present line

		text_in_window =  actions.user.tutorial_draft_get_text()

		if (text_in_window !=  "Say 'Next Line to go to the next line.  Say 'last line' to go to the last line."):
			present_line = text_in_window
	


		#append present line to past.txt 
		with open (os.path.join(__location__, 'past.txt'),'a') as pastout:  

			pastout.writelines(present_line)
			pastout.close()

		# get the last 10 lines of past.txt for display

		with open (os.path.join(__location__, 'past.txt'),'r') as pastin:
			past_lines = pastin.read().splitlines(True)
			past_ten_lines = past_lines[-10:]
			pastin.close()

		#get the top line of future.txt 
		     # Todo if line is blank, append it to past.txt and continue until next sentence is reached
			
		top_line = ""

		with open(os.path.join(__location__, 'future.txt'), 'r') as fin:
			future_data = fin.read().splitlines(True)
			#store top line of future file in
			top_line = future_data[0]
			# paste top line of future.txt into the draft window,

			fin.close()

		with open(os.path.join(__location__, 'future.txt'), 'w') as fout:
		     # delete the top line from future.txt and save file
		     future_data = future_data[1:]
		     fout.writelines(future_data)
		     fout.close()

		# get the top 10 lines of future file for display
		future_ten_lines = future_data[:10]

		with open (os.path.join(__location__, 'present_line.txt'),'w') as presentout:
			presentout.writelines(top_line)
			presentout.close()
		
		with open (os.path.join(__location__, 'present_line.txt'),'r') as presentin:
			current_line = presentin.read().splitlines(True)
			presentin.close()


		actions.user.tutorial_draft_show(current_line[0])



	def write_note():
		"""write a note"""		
		global past_ten_lines
		global present_line
		global latest_line

		# save past file
		with open (os.path.join(__location__, 'past.txt'),'r') as pastin: 
			past_data = pastin.read().splitlines(True)
			current_step = [actions.user.tutorial_draft_get_text()+"\n"]

			truncated_past_data = past_data[0:10]
			past_ten_lines = truncated_past_data
			print("******************************")
			print(str(past_ten_lines))
			#past_ten_lines=truncated_past_data
			pastin.close()
		
		#get curret step from draft window and write it to file.  Then write the rest of the data below it. 
		with open (os.path.join(__location__, 'past.txt'),'w') as pastout: 
			current_step = actions.user.tutorial_draft_get_text()

			sentences = re.split('[\n.]', current_step) 

			if len(sentences) > 1:
				print("--------------------------------------------------------")
				print(sentences)
				print(sentences[0])
				#pastout.writelines(sentences[0])
				remaining_sentences = sentences[1:]
				print(str(remaining_sentences))
				#print(remaining_sentences)
				clipboard = ".".join(remaining_sentences)
				print(clipboard)
				actions.user.tutorial_draft_show(clipboard) 

				present_line = clipboard
				latest_line = sentences[0]		
				pastout.writelines(sentences[0] + ".\n")
			else: 
				present_line = current_step
			
			pastout.writelines(past_data)
			pastout.close() 

	def write_newline():
		"""Insert newlines into past file"""
		global past_ten_lines
		global present_line
		global latest_line
		with open (os.path.join(__location__, 'past.txt'),'r') as pastin: 
			past_data = pastin.read().splitlines(True)
			current_step = [actions.user.tutorial_draft_get_text()+"\n"]

			truncated_past_data = past_data[0:10]
			past_ten_lines = truncated_past_data
			print("******************************")
			print(str(past_ten_lines))
			#past_ten_lines=truncated_past_data
			pastin.close()
		
		with open (os.path.join(__location__, 'past.txt'),'w') as pastout: 
			pastout.writelines("\n")
			pastout.writelines(past_data)
			pastout.close()

	def show_future():
		"""shows the upcoming ten lines"""
		global future_ten_lines
		     # delete the top line from future.txt and save file
		with open(os.path.join(__location__, 'future.txt'), 'r') as fin:
			future_data = fin.read().splitlines(True)
			future_ten_lines = future_data[:10]
			fin.close()
		future.show()

	def hide_future():
		"""hides the upcoming ten lines"""
		future.hide()

	def show_past():
		"""shows the past ten lines"""
		global past_ten_lines
		     # delete the top line from future.txt and save file
		with open(os.path.join(__location__, 'past.txt'), 'r') as pin:
			past_data = pin.read().splitlines(True)
			past_ten_lines = past_data[-10:]
			pin.close()

		past.show()

	def hide_past():
		"""hides the past ten lines"""
		past.hide()



