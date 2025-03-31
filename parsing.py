import xml.etree.ElementTree as ET
import os
import shelve
from tkinter import *

from entities import *

def parse_images(root):
	children = os.scandir('raw')
	
	for child in children:
		if child.path.endswith(".xml") and child.is_file():
			tree = ET.parse(child)
			tree_root = tree.getroot()
			
			if tree_root.tag == "Images":
				for image in tree_root.findall("Image"):
					id = image.find("ID").text
					
					img_path = image.find("Path").text
					
					root.images[id] = img_path
					
def parse_xml(game):
	raw_data = shelve.open(game.save_path + "/raw_data")
	
	children = os.scandir('raw')
	
	for child in children:
		if child.path.endswith(".xml") and child.is_file():
			tree = ET.parse(child)
			root = tree.getroot()
			
			try:
				xml_dict[root.tag](raw_data, root)
				
			except KeyError:
				pass
	
	raw_data.close()
	
	game.load_data()

def get_dict(file, key):
	try:
		dict = file[key]
		
	except:
		dict = {}
		
	return dict
	
def parse_classes(file, root):
	class_dict = get_dict(file, "class_dict")
	
	for class_ in root.findall("Class"):
		id = class_.find("ID").text
		
		name = class_.find("Name").text
		
		obj = Class(
			id,
			name,
		)
		
		class_dict[id] = obj
		
	file["class_dict"] = class_dict
	
def parse_races(file, root):
	race_dict = get_dict(file, "race_dict")
	
	for race in root.findall("Race"):
		id = race.find("ID").text
		
		name = race.find("Name").text
		
		name_prefixes_node = race.find("Name_Prefixes")
		name_prefixes = []
		for name_prefix_node in name_prefixes_node.findall("Name_Prefix"):
			name_prefixes.append(name_prefix_node.text)
			
		name_vowels_node = race.find("Name_Vowels")
		name_vowels = []
		for name_vowel_node in name_vowels_node.findall("Name_Vowel"):
			name_vowels.append(name_vowel_node.text)
		
		name_suffixes_node = race.find("Name_Suffixes")
		name_suffixes = []
		for name_suffix_node in name_suffixes_node.findall("Name_Suffix"):
			name_suffixes.append(name_suffix_node.text)
			
		masc_portraits_node = race.find("Masc_Portraits")
		masc_portraits = []
		for masc_portrait_node in masc_portraits_node.findall("Masc_Portrait"):
			masc_portraits.append(masc_portrait_node.text)
			
		fem_portraits_node = race.find("Fem_Portraits")
		fem_portraits = []
		for fem_portrait_node in fem_portraits_node.findall("Fem_Portrait"):
			fem_portraits.append(fem_portrait_node.text)
		
		obj = Race(
			id,
			name,
			name_prefixes,
			name_vowels,
			name_suffixes,
			masc_portraits,
			fem_portraits,
		)
		
		race_dict[id] = obj
		
	file["race_dict"] = race_dict
	
def parse_naming_systems(file, root):
	naming_system_dict = get_dict(file, "naming_system_dict")
		
	for naming_system in root.findall("NamingSystem"):
		id = naming_system.find("ID").text
		
		name = naming_system.find("Name").text
		
		parts = []
		required = []
		space = []
		for part_node in naming_system.findall("Part"):
			parts.append([name.text for name in part_node.findall("Name")])
			
			required.append(int(part_node.get("required")))
			
			space.append(part_node.get("space"))
			
		obj = NamingSystem(
			id,
			name,
			parts,
			required,
			space,
		)
		
		naming_system_dict[id] = obj
		
	file["naming_system_dict"] = naming_system_dict
	
xml_dict = {
	"Classes": parse_classes,
	"NamingSystems": parse_naming_systems,
	"Races": parse_races,
}