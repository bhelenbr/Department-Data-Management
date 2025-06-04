#!/usr/bin/python3

# Python code to scatter file to faculty folder
# First argument is file to scatter, second argument is Faculty folder, third argument is subfolder name i.e.
# scatter <file to scatter> <Faculty folder> <Subfolder>\\


import os
import shutil
import sys
import platform

# Destination is faculty folder
if platform.system() == 'Windows':
	file_destination = r"S:\departments\Mechanical & Aeronautical Engineering\Faculty"
else:
	file_destination = r"/Volumes/Mechanical & Aerospace Engineering/Faculty"
	
# Graphically select file to scatter
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
root = tk.Tk()
root.withdraw()
source = filedialog.askopenfilename(title='Select file to scatter to Faculty directories')

# Graphically ask for subfolder name
subfolder = tk.simpledialog.askstring('Name of Subfolder', 'Type name')

print(subfolder)
os.chdir(file_destination) # changes directory to that of the file destination

for FacultyName in os.listdir(file_destination): # For each faculty member
    if not FacultyName.startswith('.'): # gets rid of hidden files generated, allows for only faculty names left
        list = os.listdir(FacultyName+os.sep+subfolder) # provides list of files in subfolder of each faculty member
        if not os.path.basename(source) in list: # if the excel file not in list
        	shutil.copy(source, FacultyName +os.sep +subfolder) # move file to desired folder if doesn't exist

