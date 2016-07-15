# usage: 
# python AtomicNature.py 25 0.7 25.0 data

import sys
import numpy as np
import skimage.io
from skimage.measure import label, regionprops
import os
import matplotlib.pyplot as plt

def get_blobs(img_filename, threshold, min_area):
	img = skimage.io.imread(img_filename, as_grey=True)

	thresh_img = np.zeros(img.shape)
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			if img[i,j] > threshold:
				thresh_img[i,j] = 1
			else:
				thresh_img[i,j] = 0
	# Note: the above 7 lines can be done in a single line
	# but I wanted you to practice using nested loops.
	# Here is the one-line version:
	# thresh_img = img > threshold

	label_img = label(thresh_img)
	regions = regionprops(label_img)

	blobs = []
	for props in regions:
		if props.area >= min_area:
			blobs.append((props.centroid[1],props.centroid[0])) # x and y are swapped
	return blobs
	# print 'Found %d blobs' % count

def closest(blobs, query):
	distances = np.zeros(len(blobs))
	for i,b in enumerate(blobs):
		distances[i] = np.sqrt((b[0]-query[0])**2 + (b[1]-query[1])**2)
	return min(distances) 

def main():
	min_area  = int(sys.argv[1])
	threshold = float(sys.argv[2])
	max_move  = float(sys.argv[3])
	directory = sys.argv[4]

	displacements = list()
	last_blobs = list()
	for filename in os.listdir(directory):
		full_path = os.path.join(directory, filename)
		filename, file_extension = os.path.splitext(full_path)
		if file_extension != '.jpg':
			continue

		# print 'Processing image %s' % full_path
		blobs = get_blobs(full_path, threshold, min_area)	
		# print 'Found %d blobs' % len(blobs)
		
		if last_blobs:
			for b in blobs:
				dist = closest(last_blobs, b)
				if dist <= max_move:
					displacements.append(dist)

		last_blobs = blobs
	
	# print 'Found %d displacements' % len(displacements)
	# print 'min=%f, max=%f, mean=%f' % (np.min(displacements), np.max(displacements), np.mean(displacements))

	r = np.array(displacements)
	r *= 0.175e-6 # conversion from microns to meters
	sigma_hat2 = 0.5*np.sum(r**2)/len(r)
	dt = 0.5 # time between frames (seconds)
	T = 297 # Temperature (Kelvin)
	eta = 9.135e-4  # viscosity
	radius = 0.5e-6 # bead radius (meters)
	R = 8.31457  # gas constant
	D = sigma_hat2*0.5/dt
	k = D*6.0*np.pi*eta*radius/T
	print "Estimate of Boltzmann's constant: %.4g J/K" % k
	NA = R/k
	print "Estimate of Avogadro's number:    %.4g" % NA

def test_get_blobs():
	blobs = get_blobs('../data/run_1/frame00001.jpg', 0.7, 25)
	print 'Found %d beads:' % len(blobs)
	for blob in range(len(blobs)):
		blob = blobs[blob]
		print '(%6.2f, %6.2f)' % (blob[0], blob[1])

if __name__ == "__main__":
	# test_get_blobs()
	main()