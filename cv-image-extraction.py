# image extraction script for Pexels db

# RGB dataset:  https://www.kaggle.com/datasets/innominate817/pexels-110k-768p-min-jpg
# D dataset:    https://www.kaggle.com/datasets/innominate817/pexels-110k-768p-min-jpg-depth-dpt-hybrid

# This script extracts SET_SIZE images which contain depth maps
# i.e., images in from ./d/images are matched with ./rgb/images
# and this is saved into ./output

SET_SIZE = 5000	# Set this for the size of the set



from os import listdir
from os.path import isfile, join
from os import system
d_path = "./d/images"
d_files = [f for f in listdir(d_path) if isfile(join(d_path, f))]
rgb_path = "./rgb/images"
rgb_files = [f for f in listdir(rgb_path) if isfile(join(rgb_path, f))]

rgb_queries = {}

for rgb in rgb_files:
	rgb_queries[rgb.split(".")[0].split("-")[-1]] = rgb

i = 0
for f in d_files:
	i += 1
	if i >= SET_SIZE:
		break
	q =f.split(".")[0].split("-")[1]
	try:
		system("cp ./rgb/images/" + rgb_queries[q] + " ./output/" + q + "-rgb.jpg")
		system("cp ./d/images/depth-" + q + ".jpeg ./output/" + q + "-depth.jpeg")
	except:
		print("oops at ", q)


