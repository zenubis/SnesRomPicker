import sys;
import glob;
import os;

def processDir(path):
	print "processDir:", path;
	files = glob.glob(path + os.path.sep + "*");

	for file in files:
		if os.path.isdir(file):
			processDir(file);
		else:
			print "file -", file;


if len(sys.argv) <= 1:
	print "Error: Please specify path to scan.";
	exit(1);

if not os.path.isdir(sys.argv[1]):
	print "Error: path is not a directory -", sys.argv[1];
	exit(1);

processDir(sys.argv[1]);

