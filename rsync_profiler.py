#!/usr/bin/python
# -*- coding: utf-8 -*-

"""rsync_profiler - executes rsync with predefined arguments"""

from __future__ import print_function

__author__ = "Paweł Zacharek"
__copyright__ = "Copyright (C) 2015 Paweł Zacharek"
__date__ = "2015-11-26"
__license__ = "GPLv2+"
__version__ = "0.1.1"

import argparse

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("label", nargs="?", default=None, help="label of a profile")
parser.add_argument("-d", "--date", action="store_true", help="append date to the name of backup directory")
parser.add_argument("-f", "--file", default="rsync_profiles.txt", help="specify alternate profiles file")
parser.add_argument("-l", "--list", action="store_true", help="list all available labels")
parser.add_argument("-p", "--profiles", action="store_true", help="print a profiles file")
parser.add_argument("-s", "--time", action="store_true", help="append date and time to the name of backup directory")
parser.add_argument("-t", "--test", action="store_true", help="perform a dry-run (does not change files)")
args = parser.parse_args()

import os
import sys
import time

start_comment = "#"
delimiter = " ; "

if args.profiles:
	# print profiles
	with open(args.file) as file:
		print(file.read(), end="")
	parser.exit()

if args.list:
	# list labels
	with open(args.file) as file:
		print("\t".join([line.split(delimiter)[0] for line in file if line.lstrip() != "" and not line.lstrip().startswith(start_comment)]))
	parser.exit()

if args.label is None:
	parser.error("no label given")

# find a profile with the proper label
with open(args.file) as file:
	try:
		_, options, backup, src, dest = [line.split(delimiter) for line in file if not line.lstrip().startswith(start_comment) and line.split(delimiter)[0] == args.label][0]
	except IndexError:
		sys.exit('No label "%s" found in "%s".' % (args.label, args.file))

test = "--dry-run" if args.test else ""
time_format = "_%Y-%m-%d_%H%M%S" if args.time else "_%Y-%m-%d" if args.date else ""
backup_folder = "%s%s" % (backup, time.strftime(time_format))

# execute rsync
os.system("rsync %s %s %s %s %s" % (test, options, backup_folder, src, dest.rstrip("\n")))
