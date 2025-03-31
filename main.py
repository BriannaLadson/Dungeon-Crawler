from tkinter import *

import screens
import helpfunctions as helpf

class Root(Tk):
	def __init__(self):
		super().__init__()
		self.title("Dungeon Crawler")
		self.state("zoomed")
		
		self.font_name = "Times"
		
		self.accent_color = "#b92a13"
		self.main_color = "black"
		
		#Root Window Icon
		icon = PhotoImage(file="images/Dungeon Crawler Icon.png")
		self.iconphoto(True, icon)
		
def start(root):
	helpf.create_dir("saves")
	
	root.start_screen = screens.StartScreen(root)
		
if __name__ == "__main__":
	root = Root()
	
	start(root)
	
	root.mainloop()