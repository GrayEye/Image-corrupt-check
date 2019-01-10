#This program will scan a directory and all it's subdirectories for corrupted jpg, png, gif, and bmp images and collect them in a Catch folder

#To run this program you will need to install Python 2.7 and PILLOW
#Once installed save this file in a notepad document with the .py extension
#Then run cmd.exe and type the following: C:\Python27\python.exe "C:\Directory this is saved in\this.py" "C:\Directory to be scanned"
#You must make a folder called Catch in your root C:\ directory for the corrupted images to be collected in


#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# vi:ts=4 sw=4 et

# Okay, this code is a bit ugly, with a few "anti-patterns" and "code smell".
# But it works and I don't want to refactor it *right now*.

# TODO:
#  * Refactor it a little
#  * Add support for custom filename filter (instead of the hardcoded one)

#Big thanks to denilsonsa for writing most of this code at https://bitbucket.org/denilsonsa/small_scripts/src/542edd54d290d476603e939027ca654b25487d85/jpeg_corrupt.py?at=default


import getopt
import fnmatch
import re
import os
import os.path
import sys
import PIL.Image


available_parameters = [
    ("h", "help", "Print help"),
    ("v", "verbose", "Also print clean files"),
]


class ProgramOptions(object):
    """Holds the program options, after they are parsed by parse_options()"""

    def __init__(self):
        self.globs = ['*.jpg', '*.jpe', '*.jpeg', '*.gif', '*.png', '*.bmp']
        self.glob_re = re.compile('|'.join(
            fnmatch.translate(g) for g in self.globs
        ), re.IGNORECASE)

        self.verbose = False
        self.args = []


def print_help():
    global opt
    scriptname = os.path.basename(sys.argv[0])
    print "Usage: {0} [options] files_or_directories".format(scriptname)
    print "Recursively checks for corrupt image files"
    print ""
    print "Options:"
    long_length = 2 + max(len(long) for x,long,y in available_parameters)
    for short, long, desc in available_parameters:
        if short and long:
            comma = ", "
        else:
            comma = "  "

        if short == "":
            short = "  "
        else:
            short = "-" + short[0]

        if long:
            long = "--" + long

        print "  {0}{1}{2:{3}}  {4}".format(short,comma,long,long_length, desc)

    print ""
    print "Currently (it is hardcoded), it only checks for these files:"
    print "  " + " ".join(opt.globs)


def parse_options(argv, opt):
    """argv should be sys.argv[1:]
    opt should be an instance of ProgramOptions()"""

    try:
        opts, args = getopt.getopt(
            argv,
            "".join(short for short,x,y in available_parameters),
            [long for x,long,y in available_parameters]
        )
    except getopt.GetoptError as e:
        print str(e)
        print "Use --help for usage instructions."
        sys.exit(2)

    for o,v in opts:
        if o in ("-h", "--help"):
            print_help()
            sys.exit(0)
        elif o in ("-v", "--verbose"):
            opt.verbose = True
        else:
            print "Invalid parameter: {0}".format(o)
            print "Use --help for usage instructions."
            sys.exit(2)

    opt.args = args
    if len(args) == 0:
        print "Missing filename"
        print "Use --help for usage instructions."
        sys.exit(2)


def is_corrupt(imagefile):
    """Returns None if the file is okay, returns an error string if the file is corrupt."""
    #http://stackoverflow.com/questions/1401527/how-do-i-programmatically-check-whether-an-image-png-jpeg-or-gif-is-corrupted/1401565#1401565
    try:
        im = PIL.Image.open(imagefile)
        im.verify()
    except Exception as e:
        return str(e)
    return None


def check_files(files):
    """Receives a list of files and check each one."""
    global opt
    i = 0
    for f in files:
        # Filtering JPEG, GIF, PNG, and BMP images
        i=i+1
        if opt.glob_re.match(f):
            status = is_corrupt(f)
            if opt.verbose and status is None:
                status = "Ok"
            if status:
                file = "{0}".format(f, status)
                print file
                shorthand = file.rsplit('\\', 1)
                extention =shorthand[1]
                fullFileName = "C:\Catch" + "\\" + extention
                os.rename(file, fullFileName)


def main():
    global opt
    opt = ProgramOptions()
    parse_options(sys.argv[1:], opt)

    for pathname in opt.args:
        if os.path.isfile(pathname):
            check_files([pathname])
        elif os.path.isdir(pathname):
            for dirpath, dirnames, filenames in os.walk(pathname):
                check_files(os.path.join(dirpath, f) for f in filenames)
        else:
            print "ERROR: '{0}' is neither a file or a dir.".format(pathname)


if __name__ == "__main__":
    main()