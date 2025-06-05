#! /usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
from datetime import date

def main(argv,years):
	source = argv[1] # file to read
	try:
		df = pd.read_excel(source,header=0)
	except OSError:
		print("Could not open/read file: " + source)
		sys.exit()
	
	today = date.today()
	year = today.year
	begin_year = year - years

	df = df[(df['Calendar Year'] >= begin_year)]
	df = df.reset_index()
	
	professional = df[(df['Type'] == 'Professional')]
	community = df[(df['Type'] == 'Community')]
	university = df[(df['Type'] == 'University') | (df['Type'] == 'Department')]
	
	table = professional.pivot_table(values=['Hours/Semester'], index=['FacultyName'], aggfunc={'Hours/Semester': 'sum'},observed=False)
	table.columns=['Prof. Service']
	new_df = table
 
	# creating the bar plot
	fig = plt.figure(figsize = (10, 5))
	plt.bar(table.index, table['Prof. Service'], color ='blue',
			width = 0.4)
	plt.xticks(rotation = 90) # Rotates X-Axis Ticks by 45-degrees
	plt.xlabel("Faculty")
	plt.ylabel("Professional Service Hours")
	plt.ylim([0,300])
	plt.savefig('Tables/professional_service.png',bbox_inches='tight',pad_inches=1)
	plt.close()
	
	table = community.pivot_table(values=['Hours/Semester'], index=['FacultyName'], aggfunc={'Hours/Semester': 'sum'},observed=False)
	table.columns=['Comm. Service']
	new_df = pd.concat([new_df, table],axis=1)

	# creating the bar plot
	fig = plt.figure(figsize = (10, 5))
	plt.bar(table.index, table['Comm. Service'], color ='blue',
			width = 0.4)
	plt.xticks(rotation = 90) # Rotates X-Axis Ticks by 45-degrees
	plt.xlabel("Faculty")
	plt.ylabel("Community Service Hours")
	plt.savefig('Tables/community_service.png',bbox_inches='tight',pad_inches=1)
	plt.close()
	
	table = university.pivot_table(values=['Hours/Semester'], index=['FacultyName'], aggfunc={'Hours/Semester': 'sum'},observed=False)
	table.columns=['U. Service']
	new_df = pd.concat([new_df, table],axis=1)

	# creating the bar plot
	fig = plt.figure(figsize = (10, 5))
	plt.bar(table.index, table['U. Service'], color ='blue',
			width = 0.4)
	plt.xticks(rotation = 90) # Rotates X-Axis Ticks by 45-degrees
	plt.xlabel("Faculty")
	plt.ylabel("University Service Hours")
	plt.ylim([0,1000])
	plt.savefig('Tables/university_service.png',bbox_inches='tight',pad_inches=1)
	plt.close()
	
	return(new_df)
	
if __name__ == "__main__":
	main(sys.argv,3)