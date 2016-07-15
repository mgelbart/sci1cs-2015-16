"""
Name:            
Student Number:  
Bamfield Number: 
Collaborators:   
"""

import sys
import numpy as np
import skimage.io
import skimage.measure
import os
# You may add more imports here if you wish.

# You may add more functions here if you wish, but, if you do, you must supply
# the comment at the top (in the same format as those below).

# Finds the blobs in an image.
# Inputs:  img_filename (string) the path to the image file
#          threshold    (float)  value to threshold images (between 0 and 1)
#          min_area     (int)    minimum area to be considered a blob (pixels^2)
# Outputs: a list containing all the blobs, each represented with its x-y coordinates
def get_blobs(img_filename, threshold, min_area):
    img = skimage.io.imread(img_filename, as_grey=True)
    # TODO
    return []

# Finds the closest point to a query point from a list of points.
# Inputs:  points (list)  the list of points to search
#          query  (tuple) the query point (represented as its x-y coordinates)
# Outputs: the Euclidean distance between the query point and the closest point to it
def closest(points, query):
    # TODO
    return 0

def main():
    # check for 5 command-line args
    if len(sys.argv) != 5:
        print "Usage: python AtomicNature.py [min_area] [threshold] [max_move] [directory]" 
        return

    # read in command-line arguments
    min_area  = int(sys.argv[1])
    threshold = float(sys.argv[2])
    max_move  = float(sys.argv[3])
    directory = sys.argv[4]

    # loop over JPEG images in the directory
    for filename in sorted(os.listdir(directory)):
        full_path = os.path.join(directory, filename)
        filename, file_extension = os.path.splitext(full_path)
        if file_extension != '.jpg':
            continue

        print 'Processing image %s' % full_path

        # get blobs in image, and then, for each one, track back to previous image
        # TODO
    
    # given the distances traveled by the blobs, estimate Avogadro's number
    # TODO

    # print out the results
    k = 0.0 # Boltzmann
    NA = 0.0 # Avogadro
    print "Estimate of Boltzmann's constant: %.4g J/K" % k
    print "Estimate of Avogadro's number:    %.4g" % NA

# A function that tests your get_blobs function. You can use this to check
# whether your get_blobs is working by comparing with the sample output supplied
# in the assignment document.
def test_get_blobs():
    blobs = get_blobs(os.path.join('data','frame00001.jpg'), 0.7, 25)
    print 'Found %d beads:' % len(blobs)
    for blob in blobs:
        print '(%6.2f, %6.2f)' % (blob[0], blob[1])

main()