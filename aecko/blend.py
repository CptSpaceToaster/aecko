#!/usr/bin/env python3.4
"""
blend.py

Written in a wonderful flurry of activitiy with contributions from
  coldsxu,
  cptspacetoaster,
  darktwister,
  luna,
  sikraemer,
  and
  simpl4
"""
# System
import os
import argparse
import subprocess
import concurrent.futures
import natsort

# Local
import aecko


def doCompare(lastFile, currentFile, outFile):
    print('Processing: "{0}" vs "{1}"...'.format(lastFile, currentFile))

    # Run given command in a subprocess
    # We might want to add the argument: ',stderr=subprocess.STDOUT'
    proc = subprocess.Popen(['compare', lastFile, currentFile, outFile])

    # Wait for the result (This will print output to stdout)
    proc.communicate()

    # Do we have an error?
    if proc.returnCode != 0:
        print('Process returned error code = {0}.'.format(proc.returnCode))


# Main code (also make it look like C? :p)
def main():
    # Parse the CL arguments
    parser = argparse.ArgumentParser(prog=aecko.CLI, description=aecko.DESCRIPTION)
    parser.add_argument('-p', '--path', dest='imagePath', default='.',
                        help='Path to the directory with images. (default=".")')
    parser.add_argument('-o', '--output', dest='outputPath', default='./out',
                        help='Path to output images to. (default="./out")')
    parser.add_argument('-w', '--workers', dest='numberOfWorkers', type=int, default=10,
                        help='Number of threads to open simultaneously. (default=10)')
    args = parser.parse_args()

    # Create the output directory if it doesn't exist already
    os.makedirs(args.outputPath, exist_ok=True)

    # Variable to keep track of the last frame in sequence
    lastFile = None

    # Counter for naming purposes
    frameNo = 0

    # Fetch the frames
    files = os.listdir(args.imagePath)
    print('Found {0} files!'.format(len(files)))

    # Initialize the threadpool
    pool = concurrent.futures.ThreadPoolExecutor(args.numberOfWorkers)

    for filename in natsort.natsorted(files):
        # Skip the first frame, because there's no previous image (check that first frame is an image)
        if not lastFile and filename.endswith('.png'):
            lastFile = filename
            continue

        # Do image diff processing
        if filename.endswith('.png'):
            # Add another job to the threadpool!  It will munch through all of the jobs we give it as time passes
            pool.submit(doCompare, lastFile, filename, '{0}/{1}-{2}_compare.jpg'.format(args.outputPath, frameNo - 1, frameNo))

            # Update the last file and frame count variables
            lastFile = filename
            frameNo += 1

    pool.shutdown(wait=True)
    print('Finished!')


if __name__ == '__main__':
    main()
