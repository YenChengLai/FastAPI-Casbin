#!/bin/bash

# Loop through all executable files in .cmds folder
for script in .cmds/*; do
    # Check if the file is executable
    if [ -x "$script" ]; then
        echo "Running $script"
        # Source the script to run it in the current shell
        source "$script"
    fi
done
