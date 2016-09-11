#!/usr/bin/python
# -*- coding: utf-8 -*-

"""rsync_profiler - executes rsync with predefined arguments"""

from __future__ import print_function

__author__ = "Paweł Zacharek"
__copyright__ = "Copyright (C) 2015-2016 Paweł Zacharek"
__date__ = "2016-09-11"
__license__ = "GPLv2+"
__version__ = "0.1.5"

import argparse
import os
import sys
import time

profiles = os.path.join(sys.path[0], "rsync_profiles.txt")
start_comment = "#"
delimiter = " ; "

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("label", nargs="?", default=None, help="label of a profile")
parser.add_argument("-d", "--date", action="store_true", help="append date to the name of backup directory")
parser.add_argument("-f", "--file", default=profiles, help="specify alternate profiles file")
parser.add_argument("-l", "--list", action="store_true", help="list all available labels")
parser.add_argument("-p", "--profiles", action="store_true", help="print a profiles file")
parser.add_argument("-s", "--time", action="store_true", help="append date and time to the name of backup directory")
parser.add_argument("-t", "--test", action="store_true", help="perform a dry-run (does not change files)")
args = parser.parse_args()

if not os.path.isfile(args.file):
	parser.error('file "%s" not found' % args.file)

if args.profiles:
	# print profiles
	with open(args.file) as file:
		print(file.read(), end="")
	parser.exit()

if args.list:
	# list labels
	with open(args.file) as file:
		print("\t".join([
			line.split(delimiter)[0].strip() for line in file
			if line.strip() != "" and not line.lstrip().startswith(start_comment)
		]))
	parser.exit()

if args.label is None:
	parser.error("no label given")

# find a profile with the proper label
with open(args.file) as file:
	try:
		_, options, backup, src, dest = [
			line.split(delimiter) for line in file
			if not line.lstrip().startswith(start_comment) and line.split(delimiter)[0].strip() == args.label
		][0]
	except IndexError:
		parser.error('No label "%s" found in "%s".' % (args.label, args.file))
	except ValueError:
		parser.error('Invalid syntax in "%s".' % args.file)

test = "--dry-run" if args.test else ""
time_format = "_%Y-%m-%d_%H%M%S" if args.time else "_%Y-%m-%d" if args.date else ""
backup_folder = "%s%s" % (backup, time.strftime(time_format))

# execute rsync
os.system("rsync %s %s %s %s %s" % (test, options, backup_folder, src, dest.rstrip("\n")))
