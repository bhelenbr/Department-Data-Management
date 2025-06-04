#! /usr/bin/env python3

# Python code to merge xlsx files
import pandas as pd
import os
import sys
from pathlib import Path
import argparse

parser = argparse.ArgumentParser(description='This script merges Excel files')
parser.add_argument('files', nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('-l', '--lines',default=0,type=int,help='the number of lines to skip')
args = parser.parse_args()
 
bigdata = pd.DataFrame() 
for file in args.files:
	df = pd.read_excel(file,skiprows=args.lines)
	bigdata = pd.concat([bigdata, df],ignore_index=True)
bigdata.to_excel('merged.xlsx',index=False)