#! /usr/bin/env python3
# import modules
import os,sys,platform,shutil
import pandas as pd
import re
import xlrd
from pathlib import Path

from make_cv.stringprotect import abbreviate_name_list

source = sys.argv[1]
facultyFolder = sys.argv[2]
df = pd.read_excel(source,skiprows=1)
df.fillna(value={"Advisor Name":""},inplace=True)
print(df.columns)
destination = "Service" +os.sep +"advisee counts.xlsx"

os.chdir(facultyFolder) # changes directory to Faculty folder

for FacultyName in os.listdir("."):
	if FacultyName.find(",") > -1:
		print(FacultyName)
		lastname = FacultyName[0:FacultyName.find(",")]
		
		# Get entries for this faculty
		entries=df[df["Advisor Name"].apply(lambda x: x.find(lastname) > -1)]
		if entries.shape[0] > 0:
			toAppend = entries[["Advisor Name","Count Distinct Name","YEAR"]]			
			filename = FacultyName +os.sep +destination
			if Path(filename).is_file():
				excelFile = pd.read_excel(filename)
				result = pd.concat([excelFile, toAppend],ignore_index=True)
				result = result.drop_duplicates()
				result.sort_values(by=['YEAR'],ascending=[True],inplace=True)
				
				backupfile = FacultyName +os.sep +"Service" +os.sep +"advisee_backup.xlsx"
				shutil.copyfile(filename,backupfile)
				
				with pd.ExcelWriter(filename) as writer:
					result.to_excel(writer,index=False)
			else:
				with pd.ExcelWriter(filename) as writer:
					toAppend.to_excel(writer,index=False)
