#!/usr/bin/env python
# Script to rename column headers in proposals & grants excel file

import os
import pandas as pd
import platform
import sys
import shutil
import xlsxwriter

new_column_names = { 
'Proposal': 'Proposal_ID',
'Long Descr': 'Title',
'P_STATUS': 'Role' 
}

# Destination is faculty folder
if platform.system() == 'Windows':
    faculty_folder = r"S:\departments\Mechanical & Aerospace Engineering\Faculty"
else:
    faculty_folder = r"/Volumes/Mechanical & Aerospace Engineering/Faculty"

filestring = "Proposals & Grants/Proposals & Grants.xlsx"
backupstring = "Proposals & Grants/p_g_old.xlsx"

for FacultyName in os.listdir(faculty_folder):
	if os.path.isdir(FacultyName):
		print(FacultyName)
		filename = os.path.join(FacultyName,filestring)
		backupfile = os.path.join(FacultyName,backupstring)
		shutil.copyfile(filename,backupfile)
		df = pd.read_excel(filename)
		#print(df.columns)
		# Rename the columns using the `rename` method
		# 		df.rename(columns=new_column_names, inplace=True)
		# 		# Convert columns to datetime objects
		# 		df['Begin Date'] = pd.to_datetime(df['Begin Date'])
		# 		df['End Date'] = pd.to_datetime(df['End Date']) 
		# 		df['Submit Date'] = pd.to_datetime(df['Submit Date'])
		# 		df.drop('Project', axis=1, inplace=True)
		# 		df.drop('ID', axis=1, inplace=True)
		# 		df.drop('PCT', axis=1, inplace=True)
		# 		df.drop('RO Number', axis=1, inplace=True)
		# Create an ExcelWriter object with specified date and datetime formats
		with pd.ExcelWriter(filename, date_format='YYYY-MM-DD', datetime_format='YY-MM-DD') as writer:
			df.to_excel(writer,sheet_name='Data',index=False)
