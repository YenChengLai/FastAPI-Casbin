#!/bin/bash

# Name of your virtual environment
venv_name="fastapi-casbin"

# Check if virtual environment already exists
if [ -d "$venv_name" ]; then
    echo "Deleting existing virtual environment $venv_name"
    # Deactivate and delete the existing virtual environment
    # deactivate  # Remove this line
    rm -rf "$venv_name"  # Delete the existing virtual environment directory
fi

# Create virtual environment
python3 -m venv $venv_name

# Activate virtual environment
source $venv_name/bin/activate

# Install dependencies from requirements.txt
pip install -r "$(dirname "$0")/requirements.txt"

echo "Virtual environment $venv_name created."
