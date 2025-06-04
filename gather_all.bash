#!/bin/bash

# Run this script from the "Department Data" folder

YEAR=$(date "+%Y")

# I assume this is being run in January
let YEAR=$YEAR-1

echo "Undergraduate Research"
cd "Undergraduate Research"
if [ ! -d Historical/${YEAR} ]; then
  mkdir Historical/${YEAR}
fi
mv -n "undergraduate research data.xlsx" Historical/${YEAR}
../Scripts/UR_gather.py
cd ..

echo "Service"
cd Service
if [ ! -d Historical/${YEAR} ]; then
  mkdir Historical/${YEAR}
fi
mv -n "service data.xlsx" Historical/${YEAR}
../Scripts/service_gather.py
cd ..

echo "Awards"
cd Awards
if [ ! -d Historical/${YEAR} ]; then
  mkdir Historical/${YEAR}
fi
mv -n "personal awards data.xlsx" Historical/${YEAR}
mv -n "student awards data.xlsx" Historical/${YEAR}
../Scripts/personal_awards_gather.py
../Scripts/student_awards_gather.py
cd ..

echo "Proposals & Grants"
cd "Proposals & Grants"
if [ ! -d Historical/${YEAR} ]; then
  mkdir Historical/${YEAR}
fi
mv -n "proposals & grants.xlsx" Historical/${YEAR}
../Scripts/srs_gather.py
cd ..

echo "Scholarship"
cd Scholarship
if [ ! -d Historical/${YEAR} ]; then
  mkdir Historical/${YEAR}
fi
mv -n *.xlsx Historical/${YEAR}
echo "Journal"
../Scripts/pubs_gather.py journal
echo "Invited"
../Scripts/pubs_gather.py invited
echo "Patent"
../Scripts/pubs_gather.py patent
echo "Refereed"
../Scripts/pubs_gather.py refereed
echo "Conference"
../Scripts/pubs_gather.py conference
echo "Book"
../Scripts/pubs_gather.py book
cd ..

echo "Reviewing"
cd Reviewing
if [ ! -d Historical/${YEAR} ]; then
  mkdir Historical/${YEAR}
fi
mv -n "reviews data.xlsx" Historical/${YEAR}
../Scripts/review_gather.py
cd ..

echo "Thesis"
cd Thesis
if [ ! -d Historical/${YEAR} ]; then
  mkdir Historical/${YEAR}
fi
mv -n "thesis data.xlsx" Historical/${YEAR}
mv -n "current student data.xlsx" Historical/${YEAR}
../Scripts/thesis_gather.py
../Scripts/current_grads_gather.py
cd ..