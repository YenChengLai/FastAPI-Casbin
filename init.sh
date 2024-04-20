#!/bin/bash

# Loop through all executable files in .cmds folder
for script in .cmds/*; do
    # Check if the file is executable
    if [ -x "$script" ]; then
        echo "Running $script"
        # Run the script
        "$script"
    fi
done
