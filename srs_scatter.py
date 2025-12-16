#! /usr/bin/env python3

# Python code to scatter Proposals and Grants data to faculty Proposals and Grants folder
# First argument is file to scatter, second argument is Faculty
# scatter <file to scatter> <Faculty folder>

# import modules
import pandas as pd
import os
import sys
import platform
from os.path import exists

new_column_names = {   
'Proposal': 'Proposal_ID',
'P_STATUS': 'Role',
'Name': 'Faculty', 
'Name.1': 'Sponsor',
'PROP_STATUS': 'Funded?',
'Long Descr': 'Title'
}



def merge_proposals(source,destination):
	# dest_file = destination +"test.xlsx"
	dest_file = destination
	df_new = pd.read_excel(source,header=1,index_col='Proposal')
	df_new.rename(columns=new_column_names, inplace=True)
	df_new.drop(['Project','ID','PCT','RO Number'], axis=1,inplace=True)
	if exists(destination):
		df_old = pd.read_excel(destination,index_col='Proposal_ID',sheet_name='Data')
		
		new_rows = df_new.loc[~df_new.index.isin(df_old.index)]
		df_concat = pd.concat([df_old, new_rows])
		#df_addPIs = pd.merge(df_concat, df_new['Principal Investigators'], left_index=True,right_index=True, how='left',suffixes=('_old',None))
		#df_addPIs.drop(columns=['Principal Investigators_old'],inplace=True)
		with pd.ExcelWriter(dest_file) as writer:
			#df_addPIs.to_excel(writer,sheet_name='sheet1')
			df_concat.to_excel(writer,sheet_name='Data')
	else:
		with pd.ExcelWriter(dest_file) as writer:
			df_new.to_excel(writer,sheet_name='Data')
	return

source_folder = sys.argv[1]
file_name = "proposals & grants.xlsx"
# Read the desired source file, which is the updated Proposal and Grants file with new entries

faculty_folder = sys.argv[2]

subfolder = "Proposals & Grants"

for FacultyName in os.listdir(faculty_folder):
	if os.path.isdir(os.path.join(faculty_folder,FacultyName)):
		lastname = FacultyName.lower()[0:FacultyName.find(",")];
		print(lastname)
		for file_to_append in os.listdir(source_folder):
			if file_to_append.lower().find(lastname) != -1:
				merge_proposals(source_folder +os.sep +file_to_append,faculty_folder+os.sep +FacultyName +os.sep +subfolder +os.sep +file_name)
