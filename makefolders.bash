#!/bin/bash

for file in *; do
	echo "$file"
	cd "$file"
	mkdir "Awards"
	mkdir "Classroom Visitations"
	mkdir "Conference"
	mkdir "Contract Letters"
	mkdir "CV"
	mkdir "FAR"
	mkdir "NOAs"
	mkdir "Proposals & Grants"
	mkdir "Sabbatical"
	mkdir "Scholarship"
	mkdir "Service"
	mkdir "Teaching"
	cd ..
done