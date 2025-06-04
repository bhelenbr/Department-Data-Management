#! /usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
from datetime import date
import argparse

def main(years,inputfile):
	source = inputfile # file to read
	try:
		props = pd.read_excel(source,header=0)
	except OSError:
		print("Could not open/read file: " + source)
		sys.exit()
	
	today = date.today()
	year = today.year
	begin_year = year - years

	props = props.fillna('')
	props['Year'] = props['Begin Date'].apply(lambda x: int(x[:4]))
	props = props[props['Year'].apply(lambda x: x >= begin_year)]
	table = props.pivot_table(values=['Proposal_ID'], index=['Year'], aggfunc={'Proposal_ID': 'count'},observed=False)
	table = table.reset_index()
	table.columns=['Year','Count']
 
	# creating the bar plot
	fig = plt.figure(figsize = (10, 5))
	plt.bar(table['Year'], table['Count'], color ='blue',
			width = 0.4)
	plt.xticks(rotation = 90) # Rotates X-Axis Ticks by 45-degrees
	plt.xlabel("Year")
	plt.ylabel("Proposals Submitted")
	plt.savefig('Tables_dept/proposal_count.png',bbox_inches='tight',pad_inches=1)
	plt.close()
	
	table = props.pivot_table(values=['Allocated Amt'], index=['Year'], aggfunc={'Allocated Amt': 'sum'},observed=False)
	table = table.reset_index()
	table.columns=['Year','Amt']

	# creating the bar plot
	fig = plt.figure(figsize = (10, 5))
	plt.bar(table['Year'], table['Amt'], color ='blue',
			width = 0.4)
	plt.xticks(rotation = 90) # Rotates X-Axis Ticks by 45-degrees
	plt.xlabel("Year")
	plt.ylabel("Proposal Amount Allocation")
	plt.savefig('Tables_dept/proposal_amt.png',bbox_inches='tight',pad_inches=1)
	plt.close()

	props = props[props['Funded?'].str.match('Y')]
	table = props.pivot_table(values=['Proposal_ID'], index=['Year'], aggfunc={'Proposal_ID': 'count'},observed=False)
	table = table.reset_index()
	table.columns=['Year','Count']
 
	# creating the bar plot
	fig = plt.figure(figsize = (10, 5))
	plt.bar(table['Year'], table['Count'], color ='blue',
			width = 0.4)
	plt.xticks(rotation = 90) # Rotates X-Axis Ticks by 45-degrees
	plt.xlabel("Year")
	plt.ylabel("Proposals Funded")
	plt.savefig('Tables_dept/grant_count.png',bbox_inches='tight',pad_inches=1)
	plt.close()

	table = props.pivot_table(values=['Allocated Amt'], index=['Year'], aggfunc={'Allocated Amt': 'sum'},observed=False)
	table = table.reset_index()
	table.columns=['Year','Amt']

	# creating the bar plot
	fig = plt.figure(figsize = (10, 5))
	plt.bar(table['Year'], table['Amt'], color ='blue',
			width = 0.4)
	plt.xticks(rotation = 90) # Rotates X-Axis Ticks by 45-degrees
	plt.xlabel("Year")
	plt.ylabel("Grants Amount Allocation")
	plt.savefig('Tables_dept/grant_amt.png',bbox_inches='tight',pad_inches=1)
	plt.close()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='This script outputs plots of proposal and grant activity in the last [YEARS] years')
	parser.add_argument('-y', '--years',default="3",type=int,help='the number of years to output')
	parser.add_argument('inputfile',help='the input excel file name')           
	args = parser.parse_args()
	
	main(args.years,args.inputfile)