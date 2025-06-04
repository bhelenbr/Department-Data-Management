#! /usr/bin/env python3

import os,sys,platform,shutil
import pandas as pd
import argparse

# Python code to scatter Undergraduate research data to faculty folders
# First argument is file to scatter, second argument is Faculty
# scatter <file to scatter> <Faculty folder>
parser = argparse.ArgumentParser(description='This script scatters the department committee data to the faculty service files')
parser.add_argument('file', help='the name of the file to scatter')
parser.add_argument('-y', '--year',type=int,help='the calendar year of data to be scattered')
args = parser.parse_args()


# Destination is faculty folder
if platform.system() == 'Windows':
	facultyFolder = r"S:\departments\Mechanical & Aerospace Engineering\Faculty"
else:
	facultyFolder = r"/Volumes/Mechanical & Aerospace Engineering/Faculty"

source = args.file
committees = pd.read_excel(source,sheet_name='Data')
committees = committees[committees["Calendar Year"] == args.year]

destination = "Service" +os.sep +"service data.xlsx"

os.chdir(facultyFolder) # changes directory to Faculty folder

for FacultyName in os.listdir("."):
	if FacultyName.find(",") > -1:
		print(FacultyName)
		lastname = FacultyName[0:FacultyName.find(",")]
		
		# Get entries for this faculty
		entries=committees[committees["Faculty"]==lastname]
		toAppend = entries.iloc[:,1:7]
		
		filename = FacultyName +os.sep +destination
		excelFile = pd.read_excel(filename,sheet_name=None)
		
		result = pd.concat([excelFile["Data"], toAppend],ignore_index=True)
		result = result.drop_duplicates()
		result.sort_values(by=['Calendar Year','Term','Description'],ascending=[True,False,True],inplace=True)
		
		backupfile = FacultyName +os.sep +"Service" +os.sep +"service_backup.xlsx"
		shutil.copyfile(filename,backupfile)
		
		with pd.ExcelWriter(filename) as writer:
			excelFile["Notes"].to_excel(writer,sheet_name='Notes',index=False)
			result.to_excel(writer,sheet_name='Data',index=False)
