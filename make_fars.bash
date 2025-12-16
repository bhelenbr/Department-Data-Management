#!/bin/zsh

for file in [A-Z]?*; do
	echo "$file" 
	cd "$file/CV"
	make_far
	cd ../..
done
