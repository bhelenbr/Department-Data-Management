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
from make_cv.stringprotect import abbreviate_name

new_column_names = {   
'Proposal': 'Proposal_ID',
'P_STATUS': 'Role',
'Name': 'Faculty', 
'Name.1': 'Sponsor',
'PROP_STATUS': 'Funded?',
'Long Descr': 'Title'
}

def merge_proposals(df_new, destination):
	if exists(destination):
		df_old = pd.read_excel(
			destination,
			index_col="Proposal_ID",
			sheet_name="Data"
		)

		# keep only truly new proposal IDs
		new_rows = df_new.loc[~df_new.index.isin(df_old.index)]
		print(f"adding {len(new_rows)} rows")
		# insert new rows by index
		df_old.loc[new_rows.index, new_rows.columns] = new_rows

		df_old.index.name = "Proposal_ID"

		with pd.ExcelWriter(destination) as writer:
			df_old.to_excel(writer, sheet_name="Data")

	else:
		with pd.ExcelWriter(destination) as writer:
			df_new.to_excel(writer, sheet_name="Data")


# Read the desired source file, which is the updated Proposal and Grants file with new entries
source = sys.argv[1]
df = pd.read_excel(source,index_col='Proposal',skiprows=1)
df.rename(columns=new_column_names, inplace=True)
df.drop(['Project','ID','PCT','RO Number'], axis=1,inplace=True)
df["Faculty"] = (
	df["Faculty"]
	.astype(str)
	.apply(lambda x: abbreviate_name(x,first_initial_only=True).lower())
)
df.indexname = "Proposal_ID"

faculty_folder = sys.argv[2]
subfolder = "Proposals & Grants"
file_name = "proposals & grants.xlsx"

for FacultyName in os.listdir(faculty_folder):
	pandg_folder = faculty_folder+os.sep +FacultyName +os.sep +subfolder
	if os.path.isdir(pandg_folder):
		name = abbreviate_name(FacultyName,first_initial_only=True).lower();
		entries=df[df["Faculty"]==name]
		print(f"{name}: {str(len(entries))}")
		merge_proposals(entries,faculty_folder+os.sep +FacultyName +os.sep +subfolder +os.sep +file_name)
