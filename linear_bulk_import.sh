#!/bin/bash

# Replace with the correct path to your CSV file
CSV_FILE="./linear_import_ready.csv"

# Read CSV line by line, skipping header
tail -n +2 "$CSV_FILE" | while IFS=',' read -r title description; do
  # Remove leading/trailing whitespace and quotes
  clean_title=$(echo "$title" | sed 's/^"//;s/"$//' | xargs)
  clean_description=$(echo "$description" | sed 's/^"//;s/"$//' | xargs)

  echo "Creating issue: $clean_title"
  
  lin new --title "$clean_title" --description "$clean_description"
done