#! /usr/bin/env python3

# This code will be used to transfer individual professor evaluation data to their respective data files
# from the master evaluation spreadsheet

# import modules
import pandas as pd
import os
import platform
import sys

faculty_dir = sys.argv[2]
source_file = sys.argv[1]

df = pd.read_excel(source_file)
new_columns = [ "STRM","term","school","course","course_num","course_section","course_title","INSTR_NA","count_evals","enrollment","Particip","question","a1","a1_pct","a2","a2_pct","a3","a3_pct","a4","a4_pct","a5","a5_pct","na","na_pct","Calculated Mean","Question"]
df.columns = new_columns
df["Weighted Average"] = df["count_evals"]*df["Calculated Mean"]
df["combined_course_num"] = df["course_num"]
df.fillna(value={"INSTR_NA":""},inplace=True)
sorted = df.sort_values(by="INSTR_NA",ignore_index=True)
nrows = sorted.shape[0]

os.chdir(faculty_dir) # where files need to go

count = 1
while count < nrows:
	advisor = sorted.loc[count,'INSTR_NA']
	entries=sorted[sorted["INSTR_NA"]==advisor]
	entries.reset_index(inplace=True)
	for FacultyName in os.listdir("."):
		if FacultyName[0].isalnum():
			lastname = FacultyName.lower()[0:FacultyName.find(",")]
			firstinitial = FacultyName.lower()[FacultyName.find(",")+2]
			if advisor.lower().find(lastname+","+firstinitial) != -1 :
				print(lastname+","+firstinitial)
				#print(entries.head())
				with pd.ExcelWriter(FacultyName + "/Teaching/" + "/teaching evaluation data.xlsx") as writer:
					entries.to_excel(writer,sheet_name='Data',index=False)
	count += entries.shape[0]

