#! /bin/bash

set -e

echo "Creating Python 3 virtual environment for this project..."

python3 -m venv pyenv
source pyenv/bin/activate
pip3 install --no-cache-dir --upgrade pip
pip3 install --no-cache-dir wheel
pip3 install --no-cache-dir -r requirements.txt

echo ""
echo "Done! Python envirnoment is in 'pyenv' directory"
echo ""
echo "To use the Python environment to open the project with JupyterLab,"
echo "use the following commmands from this directory:"
echo ""
echo "  source pyenv/bin/activate"
echo "  jupyter-lab"
