from tkinter import *
from tkinter import ttk
import os
import random

import helpfunctions as helpf
import parsing
import entities
import checkbox

#Screens
class StartScreen(Canvas):
	def __init__(self, root):
		self.root = root
		super().__init__(root)
		self.pack(fill=BOTH, expand=1)
		self.update()
		
		can_w = self.winfo_width()
		can_h = self.winfo_height()
		
		#Background
		self.bg_img = helpf.resize_image("images/Dungeon Crawler Start Screen.png", can_w, can_h)
		self.create_image(0, 0, anchor="nw", image=self.bg_img)
		
		btn_w = self.winfo_width() // 4
		btn_h = int(btn_w * (1080 / 1920))
		
		#New Game
		self.new_game_img = helpf.resize_image("images/New Game Button.png", btn_w, btn_h)
		self.new_game_item = self.create_image(can_w // 4 - 100, can_h // 2, image=self.new_game_img)
		
		self.new_game_hover_img = helpf.resize_image("images/New Game Button Hover.png", btn_w, btn_h)
		self.new_game_hover_item = self.create_image(can_w // 4 - 100, can_h // 2, image=self.new_game_hover_img, state="hidden")
		
		self.tag_bind(self.new_game_item, "<Enter>", lambda e: self.swap(self.new_game_item, self.new_game_hover_item))
		self.tag_bind(self.new_game_hover_item, "<Leave>", lambda e: self.swap(self.new_game_hover_item, self.new_game_item))
		self.tag_bind(self.new_game_hover_item, "<Button-1>", self.new_game)
		
		#Load Game
		self.load_game_img = helpf.resize_image("images/Load Game Button.png", btn_w, btn_h)
		self.load_game_item = self.create_image(can_w // 4 - 100, can_h // 2 + 100, image=self.load_game_img)
		
		self.load_game_hover_img = helpf.resize_image("images/Load Game Button Hover.png", btn_w, btn_h)
		self.load_game_hover_item = self.create_image(can_w // 4 - 100, can_h // 2 + 100, image=self.load_game_hover_img, state="hidden")
		
		self.tag_bind(self.load_game_item, "<Enter>", lambda e: self.swap(self.load_game_item, self.load_game_hover_item))
		self.tag_bind(self.load_game_hover_item, "<Leave>", lambda e: self.swap(self.load_game_hover_item, self.load_game_item))
		
		#Exit
		self.exit_img = helpf.resize_image("images/Exit Button.png", btn_w, btn_h)
		self.exit_item = self.create_image(can_w // 4 - 100, can_h // 2 + 200, image=self.exit_img)
		
		self.exit_hover_img = helpf.resize_image("images/Exit Button Hover.png", btn_w, btn_h)
		self.exit_hover_item = self.create_image(can_w // 4 - 100, can_h // 2 + 200, image=self.exit_hover_img, state="hidden")
		
		self.tag_bind(self.exit_item, "<Enter>", lambda e: self.swap(self.exit_item, self.exit_hover_item))
		self.tag_bind(self.exit_hover_item, "<Leave>", lambda e: self.swap(self.exit_hover_item, self.exit_item))
		self.tag_bind(self.exit_hover_item, "<Button-1>", self.exit_game)
		
	def swap(self, item, item1):
		self.itemconfig(item, state="hidden")
		
		self.itemconfig(item1, state="normal")
		
	def new_game(self, event=None):
		popup = EnterSaveNamePopup(self.root)
		popup.center()
		
	def exit_game(self, event=None):
		self.root.destroy()
		
class Screen(Frame):
	def __init__(self, root):
		self.root = root
		super().__init__(bg=root.main_color)
		self.pack(fill=BOTH, expand=1)
		
class CharacterCreationScreen(Screen):
	def __init__(self, root):
		super().__init__(root)
		
		self.game = root.game
		
		#Title
		title_fr = Frame(self, bg="black")
		title_fr.pack(fill=X)
		
		title_lbl = Label(title_fr, text="Character Creation", font=(root.font_name, 30), bg="black", fg=root.main_color)
		title_lbl.pack()
		
		#Options
		option_fr = Frame(self, bg=root.main_color)
		option_fr.pack(fill=BOTH, expand=1)
		
		self.scr_fr = ScrollableFr(option_fr, root.main_color, "black")
		self.scr_fr.pack(fill=BOTH, expand=1)
		
		#Options - Race
		race_fr = Frame(self.scr_fr.fr1, bg=root.main_color)
		race_fr.pack(fill=X)
		
		race_lbl = Label(race_fr, text="Race", font=(root.font_name, 25), bg=root.main_color, fg="black")
		race_lbl.pack()
		
		self.race_scr_fr = ScrollableFr(race_fr, root.main_color, "black")
		self.race_scr_fr.pack(fill=BOTH, expand=1)
		
		self.fill_race()
		
		#Separator
		separator = Frame(self.scr_fr.fr1, height=2, bg="black")
		separator.pack(fill=X, pady=5)
		
		#Options - Name
		name_fr = Frame(self.scr_fr.fr1, bg=root.main_color)
		name_fr.pack()
		
		name_lbl = Label(name_fr, text="Name", font=(root.font_name, 25), bg=root.main_color, fg="black")
		name_lbl.grid(row=0, column=0, columnspan=2)
		
		fname_widget = NameWidget(name_fr, "First Name", "black", root.main_color, (root.font_name, 25), self.get_random_name)
		fname_widget.grid(row=1, column=0, padx=5)
		self.fname_var = fname_widget.var
		
		lname_widget = NameWidget(name_fr, "Last Name", "black", root.main_color, (root.font_name, 25), self.get_random_name)
		lname_widget.grid(row=1, column=1)
		self.lname_var = lname_widget.var
		
		#Separator
		separator = Frame(self.scr_fr.fr1, height=2, bg="black")
		separator.pack(fill=X, pady=5)
		
		#Options - Class
		class_fr = Frame(self.scr_fr.fr1, bg=root.main_color)
		class_fr.pack()
		
		class_lbl = Label(class_fr, text="Class", font=(root.font_name, 25), bg=root.main_color, fg="black")
		class_lbl.grid(row=0, column=0)
		
		self.class_lbx = ScrollableListbox(class_fr, "single", "black", root.main_color, font=(root.font_name, 25))
		self.class_lbx.grid(row=1, column=0)
		self.fill_class_lbx()
		self.class_lbx.variable.trace_add("write", self.trace)
		
		#Continue
		self.continue_btn = Button(self, text="Continue", font=(root.font_name, 25), bg="black", fg=root.main_color, state=DISABLED)
		self.continue_btn.pack(fill=X)
		
		self.trace()
		
	def fill_race(self):
		root = self.root
		game = self.game
		
		self.race_var = StringVar()
		self.race_var.trace_add("write", self.trace)
		
		for race in game.races:
			race_sel = RaceSelect(self.race_scr_fr.fr1, race, self.race_var, 75, 75, (root.font_name, 25))
			race_sel.pack(fill=X, expand=1)
			
	def fill_class_lbx(self):
		game = self.game
		
		lbx = self.class_lbx.listbox
		
		for class_ in game.classes:
			lbx.insert("end", class_.name)
			
	def get_random_name(self, var):
		try:
			game = self.game
	
			race_obj = helpf.get_obj_by_attr_val(game.races, "name", self.race_lbx.get_selected())
		
			var.set(race_obj.get_random_name())
			
		except AttributeError:
			race_obj = random.choice(game.races)
			
			var.set(race_obj.get_random_name())
			
	def trace(self, *args):
		state = NORMAL
		
		vars = [
			self.race_var,
			self.class_lbx.variable
		]
		
		for var in vars:
			if len(var.get()) == 0:
				state=DISABLED
			
		self.continue_btn.config(state=state)
	
class CharacterCreationBasicScreen(Screen):
	def __init__(self, root):	
		super().__init__(root)
		
		self.game = game = root.game
		
		#Title
		title_fr = Frame(self, bg=root.main_color)
		title_fr.pack(fill=X)
		
		title_lbl = Label(title_fr, text="Character Creation", font=(root.font_name, 30), bg=root.main_color, fg=root.accent_color)
		title_lbl.pack()
		
		#Name
		name_fr = Frame(self, bg=root.main_color)
		name_fr.pack()
		
		self.fname_widget = NameWidget(name_fr, "First Name", root.main_color, root.accent_color, (root.font_name, 25), self.get_random_name)
		self.fname_widget.grid(row=0, column=0)
		
		self.lname_widget = NameWidget(name_fr, "Last Name", root.main_color, root.accent_color, (root.font_name, 25), self.get_random_name)
		self.lname_widget.grid(row=0, column=1)
		
		#Middle
		self.middle_fr = Frame(self, bg=root.main_color)
		self.middle_fr.pack(fill=BOTH, expand=1)
		
		#Middle - Portrait
		self.portrait_fr = Frame(self.middle_fr, bg=root.main_color)
		self.portrait_fr.pack(side=LEFT, fill=BOTH)
		
		self.portrait_back_btn = Button(
			self.portrait_fr, 
			text="<", 
			font=(root.font_name, 25), 
			fg=root.accent_color, 
			bg=root.main_color, 
			command=lambda:self.mod_portrait_int(-1),
		)
		self.portrait_back_btn.grid(row=1, column=0)
		
		self.portrait_can = Canvas(self.portrait_fr, bg="white", width=550, height=550)
		self.portrait_can.grid(row=0, column=1, rowspan=3, columnspan=2)
		
		self.portrait_forward_btn = Button(
			self.portrait_fr, 
			text=">", 
			font=(root.font_name, 25), 
			fg=root.accent_color, 
			bg=root.main_color,
			command=lambda:self.mod_portrait_int(1),
		)
		self.portrait_forward_btn.grid(row=1, column=3)
		
		self.portrait_var = IntVar(value=0)
		
		self.gender_var = IntVar()
		self.gender_var.set(random.randint(0,1))
		
		self.fem_btn = Radiobutton(self.portrait_fr, bg=root.main_color, value=0, variable=self.gender_var, fg=root.accent_color, indicatoron=False, selectcolor="white", command=self.update_portrait)
		self.fem_btn.grid(row=3, column=0, columnspan=2)
		self.fem_btn.update()
		
		self.masc_btn = Radiobutton(self.portrait_fr, bg=root.main_color, value=1, variable=self.gender_var, fg=root.accent_color, indicatoron=False, selectcolor="white", command=self.update_portrait)
		self.masc_btn.grid(row=3, column=2)
		
		try:
			self.fem_img = helpf.resize_image("images/Fem Symbol.png", 50, 50)
			self.masc_img = helpf.resize_image("images/Masc Symbol.png", 50, 50)
			
			self.fem_btn.config(image=self.fem_img, selectcolor=root.accent_color)
			self.masc_btn.config(image=self.masc_img, selectcolor=root.accent_color)
			
		except (FileNotFoundError, AttributeError):
			self.fem_btn.config(text="Female", font=(root.font_name, 25), fg=root.accent_color)
			self.masc_btn.config(text="Male", font=(root.font_name, 25), fg=root.accent_color)
			
			self.fem_btn.grid_forget()
			self.masc_btn.grid_forget()
			
			self.fem_btn.grid(row=3, column=0, columnspan=2)
			
			self.masc_btn.grid(row=3, column=2, columnspan=3)
		
		#Middle - Race
		self.race_fr = Frame(self.middle_fr, bg=root.main_color)
		self.race_fr.pack(side=LEFT, fill=BOTH, expand=1)
		
		self.race_fr1 = Frame(self.race_fr, bg=root.main_color)
		self.race_fr1.pack()
		
		self.race_back_btn = Button(self.race_fr1, text="<", bg=root.main_color, fg=root.accent_color, font=(root.font_name, 25), command=lambda:self.mod_race_int(-1))
		self.race_back_btn.pack(side=LEFT)
		
		self.race_int_var = IntVar(value=0)
		self.race_var = StringVar()
		self.race_var.set(game.races[0].name)
		
		self.race_lbl = Label(self.race_fr1, bg=root.main_color, fg=root.accent_color, textvariable=self.race_var, font=(root.font_name, 25))
		self.race_lbl.pack(side=LEFT, padx=20)
		
		self.race_forward_btn = Button(self.race_fr1, text=">", bg=root.main_color, fg=root.accent_color, font=(root.font_name, 25), command=lambda:self.mod_race_int(1))
		self.race_forward_btn.pack(side=LEFT)
		
		self.update_portrait()
		
	def get_random_name(self, var):
		try:
			game = self.game
	
			race_obj = helpf.get_obj_by_attr_val(game.races, "name", self.race_var.get())
			
			print(race_obj.name)
		
			var.set(race_obj.get_random_name())
			
		except AttributeError:
			race_obj = random.choice(game.races)
			
			var.set(race_obj.get_random_name())
			
	def mod_race_int(self, mod):
		game = self.game
		races = game.races
		
		race_int = self.race_int_var.get()
		
		race_int += mod
		
		if race_int < 0:
			self.race_int_var.set(len(races) - 1)
			
		elif race_int > len(races) - 1:
			self.race_int_var.set(0)
			
		else:
			self.race_int_var.set(race_int)
			
		self.race_var.set(races[self.race_int_var.get()].name)
		
		self.update_portrait()
		
	def mod_portrait_int(self, mod):
		game = self.game
		
		race = game.races[self.race_int_var.get()]
		
		gender = self.get_portrait_gender()
		
		portraits = getattr(race, gender + "_portraits")
		
		portrait_int = self.portrait_var.get()
		portrait_int += mod
		
		if portrait_int < 0:
			self.portrait_var.set(len(portraits) - 1)
			
		elif portrait_int > len(portraits) - 1:
			self.portrait_var.set(0)
			
		else:
			self.portrait_var.set(portrait_int)
			
		self.update_portrait()
		
	def update_portrait(self):
		game = self.game
		
		race = game.races[self.race_int_var.get()]
		
		gender = self.get_portrait_gender()
		
		portraits = getattr(race, gender + "_portraits")
		
		try:
			portrait = "images/" + portraits[self.portrait_var.get()]
			
		except IndexError:
			self.portrait_var.set(0)
			
			portrait = "images/" + portraits[self.portrait_var.get()]
		
		self.portrait_can.delete("all")
		
		self.portrait_img = helpf.resize_image(portrait, self.portrait_can.winfo_width(), self.portrait_can.winfo_height())
		
		self.portrait_can.create_image(0, 0, image=self.portrait_img, anchor="nw")
		
	def get_portrait_gender(self):
		if self.gender_var.get() == 0:
			return "fem"
			
		else:
			return "masc"
	
#Popups
class Popup(Toplevel):
	def __init__(self, root):
		super().__init__(root)
		
		self.root = root
		
		self.overrideredirect(True)
		
		self.grab_set()
		
		self.config(bg="#b92a13")
	
	def center(self):
		self.update_idletasks()
		
		sw = self.winfo_screenwidth()
		sh = self.winfo_screenheight()
		
		tw = self.winfo_width()
		th = self.winfo_height()
		
		x = (sw // 2) - (tw // 2)
		y = (sh // 2) - (th // 2)
		
		self.geometry(f"{tw}x{th}+{x}+{y}")
		
class EnterSaveNamePopup(Popup):
	def __init__(self, root):
		super().__init__(root)
		
		self.grid_rowconfigure(1, weight=1)
		
		self.var = StringVar()
		self.var.trace_add("write", self.trace)
		
		ent = Entry(self, font=(root.font_name, 30), justify="center", bg=root.accent_color, textvariable=self.var)
		ent.grid(row=0, column=0, columnspan=2)
		
		back_btn = Button(self, text="Back", command=self.destroy, font=(root.font_name, 25), bg=root.main_color, fg=root.accent_color)
		back_btn.grid(row=1, column=0, sticky="we")
		
		self.continue_btn = Button(self, text="Continue", font=(root.font_name, 25), bg=root.main_color, fg=root.accent_color, state=DISABLED, command=self.continue_)
		self.continue_btn.grid(row=1, column=1, sticky="we")
		
		self.center()
		
	def trace(self, *args):
		state = DISABLED
		
		if len(self.var.get()) > 0:
			state = NORMAL
			
		self.continue_btn.config(state=state)
		
	def continue_(self):
		root = self.root
		
		root.save_path = "saves/" + self.var.get()
		
		if not os.path.isdir(root.save_path):
			os.mkdir(root.save_path)
			
			root.start_screen.destroy()
			
			root.game = game = entities.Game(root.save_path)
			parsing.parse_xml(game)
			
			root.character_creation_basic_screen = CharacterCreationBasicScreen(root)
			
		else:
			popup = OverwriteSavePopup(root)
			popup.center()
		
		self.destroy()
		
class OverwriteSavePopup(Popup):
	def __init__(self, root):
		super().__init__(root)
		
		self.grid_rowconfigure(2, weight=1)
		
		lbl = Label(self, text="Do you want to overwrite the following save?", font=(root.font_name, 30), bg=root.accent_color)
		lbl.grid(row=0, column=0, columnspan=2)
		
		lbl1 = Label(self, text=root.save_path, font=(root.font_name, 30), bg=root.accent_color)
		lbl1.grid(row=1, column=0, columnspan=2)
		
		yes_btn = Button(self, text="Yes", font=(root.font_name, 25), bg=root.main_color, fg=root.accent_color, command=lambda: self.continue_(True))
		yes_btn.grid(row=2, column=0, sticky="we")
		
		no_btn = Button(self, text="No", font=(root.font_name, 25), bg=root.main_color, fg=root.accent_color, command=lambda: self.continue_(False))
		no_btn.grid(row=2, column=1, sticky="we")
		
		self.center()
		
	def continue_(self, bool):
		root = self.root
		
		if not bool:
			popup = EnterSaveNamePopup(self.root)
			popup.center()
			
		else:
			helpf.overwrite_dir(self.root.save_path)
			
			self.root.start_screen.destroy()
			
			root.game = game = entities.Game(root.save_path)
			parsing.parse_xml(game)
			
			root.character_creation_basic_screen = CharacterCreationBasicScreen(root)
			
		self.destroy()
		
#Widgets
class NameWidget(Frame):
	def __init__(self, parent, lbl_txt, color, color1, font, cmd=None):
		super().__init__(parent, bg=color)
		
		self.var = StringVar()
		self.var.set(lbl_txt)
		
		ent = Entry(self, textvariable=self.var, bg=color, fg=color1, font=font)
		ent.pack(side=LEFT, padx=5)
		
		self.btn = Button(self, text="?", command=lambda: cmd(self.var), bg=color, fg=color1, font=font)
		self.btn.pack(side=LEFT)
		
class RaceSelect(Frame):
	def __init__(self, parent, race, variable, can_w, can_h, font):
		super().__init__(parent)
		
		self.grid_columnconfigure(1, weight=1)
		
		self.race = race
		
		self.variable = variable
		
		can = Canvas(self, width=can_w, height=can_h, highlightbackground="black", highlightthickness=3)
		can.pack(side=LEFT, padx=(500, 10))
		
		self.img = helpf.resize_image("images/" + race.icon, can_w, can_h)
		can.create_image(0, 0, anchor="nw", image=self.img)
		
		lbl = Label(self, text=race.name, justify="center", font=font)
		lbl.pack(side=LEFT, padx=(0, 10))
		
		cbx = checkbox.Checkbox(
			self,
			checkmark_type = "xmark",
			checkmark_width = 5,
			variable = self.variable,
			value=self.race.name,
		)
		cbx.pack(side=LEFT)
			
	def get_selected(self):
		return self.variable.get()

class ScrollableFr(Frame):
	def __init__(self, parent, color, color1):
		super().__init__(parent, bg=color, highlightbackground=color1, highlightthickness=2)
		
		self.sb = Scrollbar(self, orient=VERTICAL)
		self.sb.pack(fill=Y, side=RIGHT)
		
		self.can = Canvas(self, yscrollcommand=self.sb.set, bg=color1)
		self.can.pack(side=LEFT, fill=BOTH, expand=True)
		
		self.sb.config(command=self.can.yview)
		
		self.fr1 = Frame(self.can, bg=color)
		self.fr1.bind("<Configure>", lambda e: self.can.config(scrollregion=self.can.bbox("all")))
		
		item = self.can.create_window(0, 0, window=self.fr1, anchor=NW)
		self.can.bind("<Configure>", lambda e: self.can.itemconfig(item, width=e.width))
		self.can.config(yscrollcommand = self.sb.set)
		
class ScrollableListbox(Frame):
	def __init__(self, parent, select_mode, color, color1, font, variable=None,):
		super().__init__(parent)
		
		self.variable = variable if variable else StringVar()
		
		self.listbox = Listbox(self, selectmode=select_mode, bg=color, fg=color1, font=font)
		self.listbox.pack(side=LEFT, fill=BOTH, expand=1)
		
		self.scrollbar = Scrollbar(self, orient="vertical", command=self.listbox.yview)
		self.scrollbar.pack(side=RIGHT, fill=Y)
		
		self.listbox.config(yscrollcommand=self.scrollbar.set)
		
		self.listbox.bind("<<ListboxSelect>>", self.on_select)
		
	def on_select(self, event=None):
		selected_idx = self.listbox.curselection()
		
		if selected_idx:
			selection = self.listbox.get(selected_idx)
			
			self.variable.set(selection)
			
	def get_selected(self):
		return self.variable.get() if self.variable.get() else None