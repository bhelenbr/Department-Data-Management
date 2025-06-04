#!/usr/bin/env python3

import os
import shutil
import sys
import platform

# call like this
# distribute_files.py <Folder with files> <Subfolder> <filename>

filefolder = sys.argv[1]
subfolder = sys.argv[2]
filename = sys.argv[3]

# Destination is faculty folder
if platform.system() == 'Windows':
	file_destination = r"S:\departments\Mechanical & Aerospace Engineering\Faculty"
else:
	file_destination = r"/Volumes/Mechanical & Aerospace Engineering/Faculty"
	
os.chdir(file_destination) # changes directory to that of the file destination

for FacultyName in os.listdir(file_destination):
	lastname = FacultyName.lower()[0:FacultyName.find(",")];
	print(lastname)
	for fileToMove in os.listdir(filefolder):
		if fileToMove.lower().find(lastname) != -1:
			shutil.copy(filefolder +os.sep +fileToMove,FacultyName+os.sep +subfolder +os.sep +fileToMove)
				