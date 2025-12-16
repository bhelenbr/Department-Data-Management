#! /usr/bin/env python3

import os,sys,platform,shutil
import pandas as pd
import numpy as np
import datetime
import xlsxwriter
from datetime import date

pd.options.mode.chained_assignment = None  # default='warn'

# This reads the current student data then rewrites with updated notes
# You may have to install pandas: pip3 install pandas
# Python code to scatter current student data
# First argument is file to scatter

source = sys.argv[1]
file_destination = sys.argv[2]

students = pd.read_excel(source,skiprows=1)
students = students[students["Career"]=="GRAD"]
students.drop(students.columns[7:], axis=1, inplace=True)
students = students.fillna("")
destination = "Scholarship" +os.sep +"current student data.xlsx"
os.chdir(file_destination) # changes directory to Faculty folder

for FacultyName in os.listdir("."):
	if FacultyName.find(",") > -1:
		lastnameFI = FacultyName.lower()[0:FacultyName.find(",")+1] +FacultyName.lower()[FacultyName.find(",")+2]
		entries=students[students["LN,FN"].apply(lambda x: x.lower().find(lastnameFI) != -1)]
		if entries.shape[0] > 0:
			entries["Student Name"] = entries["Last"] + ", " + entries["First Name"]
			entries["Current Program"] = entries["Acad Plan"]
			entries["Start Date"] = pd.to_datetime(str(date.today()))
			entries = entries.drop(columns=["ID","Last","First Name","Email","Acad Plan","Career","LN,FN","Email"], errors="ignore")
			print(FacultyName)
			entries.sort_values(by=['Current Program','Start Date'],inplace=True)
			print(entries)
			with pd.ExcelWriter(FacultyName +os.sep +destination,date_format='YYYY-MM-DD', datetime_format='YY-MM-DD') as writer:
				entries.to_excel(writer,sheet_name='Data',index=False)
