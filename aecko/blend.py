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
# TODO: Re-multithread this
# import concurrent.futures
import natsort
import numpy
from PIL import Image

# Local
import aecko


def diff(val1, val2, center=255):
    return int((center + val2 - val1)/2)


def do_compare(pic1, pic2):
    # TODO: What if pic1 and pic2 are actually different dimensions for some reason?
    ret = numpy.empty(pic1.shape, pic1.dtype)
    for (i1, p1), (i2, p2) in zip(numpy.ndenumerate(pic1), numpy.ndenumerate(pic2)):
        # print(i1, p1, end=', ')
        # print(i2, p2)
        # Skip the alpha component of each pixel
        if i1[2] == 3:
            ret[i1] = 255
            continue
        ret[i1] = (diff(p1, p2))
    return ret


# Main code (also make it look like C? :p)
def main():
    # Parse the CL arguments
    parser = argparse.ArgumentParser(prog=aecko.CLI, description=aecko.DESCRIPTION)
    parser.add_argument('-p', '--path', dest='image_path', default='.',
                        help='Path to the directory with images. (default=".")')
    parser.add_argument('-o', '--output', dest='output_path', default='./out',
                        help='Path to output images to. (default="./out")')
    parser.add_argument('-w', '--workers', dest='worker_no', type=int, default=10,
                        help='Number of threads to open simultaneously. (default=10)')
    parser.add_argument('-v', '--version', action='version', version=aecko.__version__)
    args = parser.parse_args()

    # Create the output directory if it doesn't exist already
    os.makedirs(args.output_path, exist_ok=True)

    # Fetch the frames
    files = os.listdir(args.image_path)
    print('Found {0} files!'.format(len(files)))

    # Initialize the threadpool
    # TODO: Re-multithread this
    # pool = concurrent.futures.ThreadPoolExecutor(args.worker_no)
    # Add another job to the threadpool!  It will munch through all of the jobs we give it as time passes
    # TODO: Re-multithread this
    # pool.submit(do_compare, last_file, filename, '{0}/{1}-{2}_compare.png'.format(args.output_path, frame_no, frameNo + 1))
    # do_compare(last_file, filename, '{0}/{1}-{2}_compare.png'.format(args.output_path, frame_no, frameNo + 1))
    walk(files, 0, args.output_path)


def walk(files, offset, output_path):
    # Counter for naming purposes
    frame_no = offset

    # Variable to keep track of the last frame in sequence
    last_file = None
    last_pic = None

    for current_file in natsort.natsorted(files):
        # Skip the first frame, because there's no previous image (check that first frame is an image)
        if not last_file and current_file.endswith('.png'):
            last_file = current_file
            last_pic = numpy.array(Image.open(current_file))
            continue

        # Do image diff processing
        if current_file.endswith('.png'):
            out_file = '{0}/{1}-{2}_compare.png'.format(output_path, frame_no, frame_no + 1)
            print('Processing: {0} vs {1}...'.format(last_file, current_file))

            pic = do_compare(last_pic, numpy.array(Image.open(current_file)))
            Image.fromarray(pic).save(out_file)

            # Update the last file and frame count variables
            last_file = current_file
            frame_no += 1

    # TODO: Re-multithread this
    # pool.shutdown(wait=True)
    print('Finished!')


if __name__ == '__main__':
    main()
