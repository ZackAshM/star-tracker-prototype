#!/usr/bin/env python3
import numpy as np
import astropy as ast
from astropy.io import fits
import argparse
import os
from os import path

pwd = "/home/anita/work/Image_Calibration"

# command line arguments
parser = argparse.ArgumentParser(description='Description: Averages FIT files. Filenames should be formatted as type#.FIT, i.e. dark1.FIT, dark2.FIT,..., bias1.FIT, bias2.FIT,... . This program assumes a resolution of (3672, 5496) pixels. An averaged bias frame is required for correctly averaging the dark and flat frames.')
parser.add_argument('num', type=int,		# no. of image files
                    help='int; total number of image files')
parser.add_argument('type', type=str,		# type of frame
                    choices=['dark', 'bias', 'science', 'flat'],
                    help='string; frame type to average')
args = parser.parse_args()

image_data = np.empty((3672,5496))
num_frames = args.num

# check for existence of bias frame average
if not path.exists("bias_avg.FIT"):
	if args.type.lower() != "bias":
		print("Error. An averaged bias frame is required for correctly averaging the dark and flat frames.")
		exit()

# open fits image files
if path.exists("bias_avg.FIT"):
	hdul_bias = fits.open("bias_avg.FIT")
	bias_data = hdul_bias[0].data
os.chdir(args.type)
for i in range(1, num_frames+1):
	hdul_temp = fits.open("{}{}.FIT".format(args.type,i))
	temp_data = hdul_temp[0].data
	if args.type.lower() != "bias":
		temp_data = temp_data - bias_data
	image_data = image_data + temp_data	# adding image values
	hdul_temp.close()

# take the average
avg = image_data / num_frames


# saving new image
hdu = fits.PrimaryHDU(avg)
os.chdir(pwd)
i = 1
while True:
	if not path.exists("{}_avg.FIT".format(args.type)):
		print("Saving new image " + "{}_avg.FIT".format(args.type) + "... ")
		hdu.writeto("{}_avg.FIT".format(args.type, i))
		quit()
	elif path.exists("{}_avg{}.FIT".format(args.type, i)):
		i = i + 1
	else: break
print("Saving new image " + "{}_avg{}.FIT".format(args.type, i) + "... ")
hdu.writeto("{}_avg{}.FIT".format(args.type, i))



