#!/usr/bin/env python2
"""
Logpuzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Google's Python Class
http://code.google.com/edu/languages/google-python-class/

Given an apache logfile, find the puzzle urls and download the images.

"""

import os
import re
import sys
import urllib
import argparse
import webbrowser


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""

    # extract urls
    text = open(filename).read()
    urls = re.findall(r'GET (\S+.jpg)', text)

    # add domain to the start of the url
    for i, url in enumerate(urls):
        urls[i] = 'http://code.google.com' + url

    # sort by last 4 characters of image filename
    return sorted(set(urls), key=lambda x: re.findall(r'\S{4}.jpg', x)[0])


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """

    # make directory if it does not exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # retrieve images
    for i, url in enumerate(img_urls):
        print('Retrieving image ' + str(i) + '...')
        urllib.urlretrieve(url, dest_dir + '/img' + str(i))

    # write html file
    with open(dest_dir + '/index.html', 'w') as htmlfile:
        htmlfile.write('<html><body>')
        for url in img_urls:
            if 'no_picture' not in url:
                htmlfile.write('<img src="' + url + '" />')
        htmlfile.write('</body></html>')
        htmlfile.close()

    # open html file
    filepath = 'file://' + os.path.dirname(os.path.realpath(
        __file__)) + '/' + dest_dir + '/index.html'
    webbrowser.open_new_tab(filepath)


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--todir',  help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parse args, scan for urls, get images from urls"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
