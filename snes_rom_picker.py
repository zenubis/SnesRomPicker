# MIT License

# Copyright (c) 2016 Nyon Yow Feng

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys;
import glob;
import os;
import re;

# suffixes and their meaning
# https://64bitorless.wordpress.com/rom-suffix-explanations/

# purpose of the program is to select the best english and japanese rom for any particular game
# selection criteria are
# 1) verified roms '[!]'
# 2) fixed roms '[f]'
# 3) alternate roms '[a]'
# 4) roms without any flag
# roms marked with '[b]' will be avoided

# to store information about a particular rom file
class CRomInfo:

	def __init__(self, path, lang, flag):
		self.path = path;
		self.lang = "";
		self.flag = [];	#to be parse into strings

		# parsing language text, assumes only 1 language
		if None != lang:
			self.lang = ""
			for count in range(0, len(lang)):
				if lang[count] == "(" or lang[count] == ")":
					continue;
				self.lang += lang[count]

		#parsing flag text
		if None != flag:
			bStartBracket = False;
			for count in range(0, len(flag)):
				if flag[count] == "[":
					bStartBracket = True;
					continue;
				if flag[count] == ']':
					bStartBracket = False;
					continue;
				if bStartBracket == True:
					bStartBracket = False;
					self.flag.append(flag[count]);
		
	def getBestFlagAsScore(self):
		best = 0;
		if None == self.flag or len(self.flag) == 0:
			return 1;

		for f in self.flag:
			if None != re.match(r'!', f):
				if best < 5:
					best = 5;
				continue;
			elif None != re.match(r'f', f, re.I):
				if best < 4:
					best = 4;
				continue;
			elif None != re.match(r'a', f, re.I):
				if best < 3:
					best = 3;
				continue;
			elif None != re.match(r'b', f, re.I):
				return -1;
		return best;


	def isBetter(self, rhs):
		if not isinstance(rhs, CRomInfo):
			return False;
		return self.getBestFlagAsScore() > rhs.getBestFlagAsScore();

	def isJapanese(self):
		return None != re.match(r'j', self.lang, re.I);
	
	def isEnglish(self):
		if re.match(r'^e$', self.lang, re.I):
			return True;
		elif re.match(r'^u$', self.lang, re.I):
			return True;
		elif re.match(r'^uk$', self.lang, re.I):
			return True;
		return False;

	def isPublicDomain(self):
		return None != re.match(r'^PD$', self.lang, re.I);

	def __str__(self):
		return "[CRomInfo] ({0:2d}) l:{1:4s} f:{2:10s} - {3}".format(self.getBestFlagAsScore(), self.lang, self.flag, self.path);
			

# To store a selection of english and japanese rom version for a particular game
class CSelection:
	def __init__(self):
		self.eng = None; # to be set with CRomInfo when it's available
		self.jp = None;  # to be set with CRomInfo when it's available
		self.skip = [];	 # games that we didn't choose, more for debugging and verifying the program choose the best ones


filteredList = {};	# hash map of CSelection with name as key


def processDir(path):
	print "processDir:", path;
	global filteredList;
	files = glob.glob(path + os.path.sep + "*");
	# files = ['C:\Users\pollyanna\Downloads\GoodSNES2.04\Zero 4 Champ RR (beta) [!].smc'];
	for thefile in files:
		if os.path.isdir(thefile):
			processDir(thefile);
		else:
			#print "file -", thefile;
			# print filename
			filename, file_extension = os.path.splitext(os.path.basename(thefile))
			if not file_extension == ".smc":
				print "skipping", thefile 
				continue;

			squareBracketStart = False;
			curveBracketStart = False;
			isName = True;

			game_name = "";
			lang = "";
			flag = "";
			
			for n in range(0,len(filename)):
				if filename[n] == '[':
					isName = False;
					squareBracketStart = True;
					flag += filename[n];
					continue;
				elif filename[n] == ']':
					isName = False;
					squareBracketStart = False;
					flag += filename[n];
					continue;
				elif filename[n] == '(':
					isName = False;
					curveBracketStart = True;
					lang += filename[n];
					continue;
				elif filename[n] == ")":
					isName = False;
					curveBracketStart = False;
					lang += filename[n];
					continue;

				if isName:
					game_name += filename[n];
				elif squareBracketStart:
					flag += filename[n];
				elif curveBracketStart:
					lang += filename[n];

			game_name.strip();
			lang.strip();
			flag.strip();
			if None == game_name:
				print "Info: Does not have file name? (", filename, ")"
				continue;

			if not game_name in filteredList:
				filteredList[game_name] = CSelection()

			rom_info = CRomInfo(thefile, lang, flag);

			if rom_info.getBestFlagAsScore() < 0:
				# we dont want any bad roms
				filteredList[game_name].skip.append(rom_info);
				continue;
			
			if None == lang:
				#no language information, if current game do not have any
				#selection yet, choose this first; else continue.
				if filteredList[game_name].eng == None and filteredList[game_name].jp == None:
					filteredList[game_name].eng = rom_info;
				continue;

			if rom_info.isEnglish():
				# is it better than any english roms we already have
				if filteredList[game_name].eng == None or not filteredList[game_name].eng.isEnglish() or rom_info.isBetter(filteredList[game_name].eng):
					if filteredList[game_name].eng != None:
						#put into skip list for reference
						filteredList[game_name].skip.append(filteredList[game_name].eng);
					filteredList[game_name].eng = rom_info;
				else:
					filteredList[game_name].skip.append(rom_info);
			elif rom_info.isJapanese():
				# is it better than any japanese roms we already have
				if filteredList[game_name].jp == None or not filteredList[game_name].jp.isJapanese() or rom_info.isBetter(filteredList[game_name].jp):
					if filteredList[game_name].jp != None:
						filteredList[game_name].skip.append(filteredList[game_name].jp);
					filteredList[game_name].jp = rom_info;
				else:
					filteredList[game_name].skip.append(rom_info);

			else:
				#not english, not japanese, default put english, if we didn't already have an english rom
				if filteredList[game_name].eng == None:
					filteredList[game_name].eng = rom_info;
				else:
					filteredList[game_name].skip.append(rom_info);

					
################ main program start ################################
if len(sys.argv) <= 1:
	print "Error: Please specify path to scan.";
	exit(1);

if not os.path.isdir(sys.argv[1]):
	print "Error: path is not a directory -", sys.argv[1];
	exit(1);

processDir(sys.argv[1]);

# print "Total files:", filecounter;
for key in sorted(filteredList.keys()):
	print key
	print "  eng    :", filteredList[key].eng
	print "  jp     :", filteredList[key].jp
	print "  skipped:"
	for rom in filteredList[key].skip:
		print "         :", rom

################ main program ends ################################