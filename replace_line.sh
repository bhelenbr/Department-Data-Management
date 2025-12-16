#!/bin/bash

# Usage: ./replace_line.sh source_file target_file search_string

# Ensure correct number of arguments
if [ $# -ne 3 ]; then
  echo "Usage: $0 source_file target_file search_string"
  exit 1
fi

# Assign input arguments to variables
source_file=$1
target_file=$2
search_string=$3

# Check if source and target files exist
if [ ! -f "$source_file" ]; then
  echo "Error: Source file '$source_file' not found."
  exit 1
fi

if [ ! -f "$target_file" ]; then
  echo "Error: Target file '$target_file' not found."
  exit 1
fi

# Find the line in source_file that begins with search_string
line_to_replace=$(grep "^$search_string" "$source_file")

if [ -z "$line_to_replace" ]; then
  echo "No line found starting with '$search_string' in source file."
  exit 1
fi

echo $search_string
echo $line_to_replace

# Replace the line in target_file
sed -i '' "s:^$search_string.*:$line_to_replace:" "$target_file"

# Confirm the replacement
echo "Line starting with '$search_string' in '$target_file' has been replaced."
