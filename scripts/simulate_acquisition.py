#!/usr/bin/env python

"""
This script will simply create symbolic links from files in an input
folder. The links will be created in an output folder and every some
time the last link will be 'touched' simulating an image that is being
acquired by the microscope.
"""

import sys, os
import time
from glob import glob

import pyworkflow.utils as pwutils


def usage(error):
    print """
    ERROR: %s
    
    Usage: simulate_acquisition.py INPUT_PATTERN OUTPUT_FOLDER
        INPUT_PATTERN: input pattern matching input files.
        OUTPUT_FOLDER: where to create the output links.
        [DELAY, default 30]: delay in seconds between file appearance
    """ % error
    sys.exit(1)    


if not len(sys.argv) in (3,4):
    usage("Incorrect number of input parameters")

inputPattern = sys.argv[1]
outputDir = sys.argv[2]
if len(sys.argv) == 4:
    delay = sys.argv[3]
else:
    delay = 30

inputFiles = glob(pwutils.expandPattern(inputPattern))
inputFiles.sort()

print "Input pattern: ", inputPattern
print "Input files: ", inputFiles
print "Delay: ", str(delay), " seconds."

print "Cleaning output directory: ", outputDir
pwutils.cleanPath(outputDir)
pwutils.makePath(outputDir)

aTime = int(delay)
n = 5
t = aTime / n
print "t=%s" % t

for f in inputFiles:
    outputPath = os.path.join(outputDir, os.path.basename(f))
    print "Linking %s -> %s" % (outputPath, f)

    for i in range(n):
        open(outputPath, 'w').close()
        time.sleep(t)
    pwutils.cleanPath(outputPath)
    pwutils.createAbsLink(f, outputPath)
