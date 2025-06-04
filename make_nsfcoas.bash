#!/bin/zsh

for file in [A-Z]?*; do
	echo "$file" 
	cd "$file/CV"
	make_nsfcoa
	cd ../..
done
