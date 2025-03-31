import random

import helpfunctions as helpf

class Game:
	def __init__(self, save_path):
		self.save_path = save_path
		
	def load_data(self):
		path = self.save_path + "/raw_data"
		
		keys = {
			"class_dict": "classes",
			"race_dict": "races",
		}
		
		for key in keys:
			data = list(helpf.get_data(path, key).values())
			
			attr = keys[key]
			
			setattr(self, attr, data)
		
#XML
class Class:
	def __init__(self, *args):
		self.id = args[0]
		
		self.name = args[1]

class Race:
	def __init__(self, *args):
		self.id = args[0]
		
		self.name = args[1]
		
		self.name_prefixes = args[2]
		
		self.name_vowels = args[3]
		
		self.name_suffixes = args[4]
		
		self.masc_portraits = args[5]
		
		self.fem_portraits = args[6]
		
	def get_random_name(self):
		prefix = random.choice(self.name_prefixes)
		vowel = random.choice(self.name_vowels)
		suffix = random.choice(self.name_suffixes)
		
		return prefix + vowel + suffix