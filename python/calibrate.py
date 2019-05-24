#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import astropy as ast
from astropy.io import fits
import argparse
import os
from os import path


# command line arguments
parser = argparse.ArgumentParser(description='Calibrate science image w/ histogram plot. This program assumes averaged dark, bias, and flat FIT files exist in the current directory with the format type_avg.FIT (i.e. dark_avg.FIT).')
parser.add_argument('science', type=str,	# science image arg
                    help='string; science image FIT file to be calibrated')
args = parser.parse_args()
# assign args
science = args.science

# Check for calibration images
if not path.exists("dark_avg.FIT") or not path.exists("bias_avg.FIT") or not path.exists("flat_avg.FIT"):
	print("Error. This program requires averaged dark, bias, and flat FIT files.")
	exit()

# open fits image files
hdul_sci = fits.open(science)
sci_data = hdul_sci[0].data
exp_sci = hdul_sci[0].header['EXPOINUS'] * 10**(-6)	# exposure in sec
hdul_sci.close()

# assumes non-science frames already averaged in different program
hdul_dark = fits.open("dark_avg.FIT")
dark_data = hdul_dark[0].data
hdul_dark.close()

hdul_bias = fits.open("bias_avg.FIT")
bias_data = hdul_bias[0].data
hdul_bias.close()

hdul_flat = fits.open("flat_avg.FIT")
flat_data = hdul_flat[0].data
hdul_flat.close()


# processing true image
dark_data = dark_data * exp_sci
sci_data = sci_data - bias_data
data = (sci_data - dark_data) / flat_data	# need to scale back to integer values

# plot and save histogram
plt.xlabel('Pixel Value')
plt.ylabel('No. of Pixels')
plt.title('Pixel Readings')

plt.hist(data.flatten(), log=True, bins=20, histtype='step', density=True)
i = 1
while True:
	if not path.exists("hist.FIT"):
		print("Saving new histogram hist.FIT... ")
		plt.savefig('hist.png')
		break
	elif path.exists("hist{}.FIT".format(i)):
		i = i + 1
	else:
		print("Saving new histogram " + "hist{}.FIT".format(i) + "... ")
		plt.savefig("hist{}.png".format(i))
		break

# saving new image
hdu = fits.PrimaryHDU(data)
i = 1
while True:
	if not path.exists("calibrated.FIT"):
		print("Saving new image calibrated.FIT... ")
		hdu.writeto("calibrated.FIT")
		break
	elif path.exists("calibrated{}.FIT".format(i)):
		i = i + 1
	else:
		print("Saving new image " + "calibrated{}.FIT".format(i) + "... ")
		hdu.writeto("calibrated{}.FIT".format(i))
		break

