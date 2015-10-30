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
import glob
import argparse
import concurrent.futures
import natsort
import numpy
from PIL import Image

# Local
import aecko


def do_compare(pic1, pic2):
    # TODO: What if pic1 and pic2 are actually different dimensions for some reason?
    # print(pic1.shape, pic1.dtype)
    # print(pic2.shape, pic2.dtype)
    if pic1.shape[2] == 3:
        return (((pic2 + 255 - pic1)//numpy.array([2, 2, 2]))).view('uint8')[:, :, ::8]
    else:
        return (((pic2 + 255 - pic1)//numpy.array([2, 2, 2, 1]))).view('uint8')[:, :, ::8]


def chunks(l, n):
    w = len(l)//n
    for i in range(0, n-1):
        yield l[i*w:i*w+w]
    yield l[n*w-w:]


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

    # Fetch the frames in a sorted fashion
    files = natsort.natsorted(glob.glob('*.png'))
    num_files = len(files)
    print('Found {0} files!'.format(num_files))

    # Initialize the threadpool
    pool = concurrent.futures.ThreadPoolExecutor(args.worker_no)

    offset = 0
    for chunk in chunks(files, args.worker_no):
        pool.submit(walk, chunk, offset, args.output_path)
        offset += num_files//args.worker_no

    # TODO: Re-multithread this
    pool.shutdown(wait=True)


def walk(files, offset, output_path):
    # Counter for naming purposes
    frame_no = offset

    # Variable to keep track of the last frame in sequence
    last_file = None
    last_pic = None
    curr_pic = None

    for current_file in natsort.natsorted(files):
        curr_pic = numpy.array(Image.open(current_file), dtype=numpy.int16)

        # Skip the first frame, because there's no previous image (check that first frame is an image)
        if not last_file and current_file.endswith('.png'):
            last_file = current_file
            last_pic = curr_pic
            continue

        # Do image diff processing
        out_file = '{0}/{1}-{2}_compare.png'.format(output_path, frame_no, frame_no + 1)
        print('Processing: {0} vs {1}...'.format(last_file, current_file))

        Image.fromarray(do_compare(last_pic, curr_pic)).save(out_file)

        # Update the last file and frame count variables
        last_file = current_file
        last_pic = curr_pic
        frame_no += 1


if __name__ == '__main__':
    main()
