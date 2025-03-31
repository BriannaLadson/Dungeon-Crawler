from PIL import Image, ImageTk
import os
import shutil
import shelve

#Data
def get_data(path, key):
	file = shelve.open(path)
	
	output = file[key]
	
	file.close()
	
	return output

def save_data(path, key, val):
	file = shelve.open(path)
	
	file[key] = val
	
	file.close()

#Dir & File
def create_dir(path):
	if not os.path.isdir(path):
		os.mkdir(path)
		
def overwrite_dir(path):
	if not os.path.isdir(path):
		os.mkdir(path)
		
	else:
		shutil.rmtree(path)
		
		os.mkdir(path)

#Images
def resize_image(img_path, width, height):
	img = Image.open(img_path)
	
	resized_img = img.resize((width, height), Image.Resampling.LANCZOS)
	
	return ImageTk.PhotoImage(resized_img)
	
#Misc.
def get_obj_by_attr_val(objs, attr, val):
	for obj in objs:
		if hasattr(obj, attr) and getattr(obj, attr) == val:
			return obj
			
	return None