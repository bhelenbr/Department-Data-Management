#! /usr/bin/env python3

# I'm not sure why I needed this

# import modules
import pandas as pd
import os
import sys
from pathlib import Path
 
# assign directory
directory = 'Teaching'
 
# iterate over files in
# that directory
files = Path(directory).glob('*.xlsx')
bigdata = pd.DataFrame() 
for file in files:
	df = pd.read_excel(file)
	semester = file.name[13:-10]
	df['Semester'] = semester
	code = file.name[-9:-5]
	df['Code']=code
	bigdata = pd.concat([bigdata, df])
bigdata.to_excel('merged.xlsx')