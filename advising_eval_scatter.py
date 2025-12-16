#! /usr/bin/env python3

# This code will be used to transfer individual professor evaluation data to their respective data files
# from the master evaluation spreadsheet

# import modules
import pandas as pd
import os
import platform
import sys
from pathlib import Path

faculty_dir = sys.argv[2]
source_file = sys.argv[1]

df = pd.read_excel(source_file)
df.fillna(value={"LN,FN":""},inplace=True)
sorted = df.sort_values(by="LN,FN",ignore_index=True)
nrows = sorted.shape[0]

os.chdir(faculty_dir) # where files need to go

count = 1
while count < nrows:
	advisor = sorted.loc[count,'LN,FN']
	entries=sorted[sorted["LN,FN"]==advisor]
	for FacultyName in os.listdir("."):
		if FacultyName[0].isalnum():
			lastname = FacultyName.lower()[0:FacultyName.find(",")]
			firstinitial = FacultyName.lower()[FacultyName.find(",")+2]
			if advisor.lower().find(lastname+","+firstinitial) != -1 :
				print(lastname+","+firstinitial)
				filename = FacultyName +os.sep +"Service" +os.sep +"advising evaluation data.xlsx"

				if Path(filename).is_file():
					excelFile = pd.read_excel(filename)
					result = pd.concat([excelFile, toAppend],ignore_index=True)
					result = result.drop_duplicates()
					result.sort_values(by=['Term'],ascending=[True],inplace=True)					
					with pd.ExcelWriter(filename) as writer:
						result.to_excel(writer,index=False)
				else:
					with pd.ExcelWriter(filename) as writer:
						entries.to_excel(writer,index=False)
	count += entries.shape[0]
