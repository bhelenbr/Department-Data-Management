#!/bin/zsh

for file in [A-Z]?*; do
	echo "$file" 
	cd "$file/make_cv/FAR"
	make_far -g 4 -q
	cd ../../..
done
