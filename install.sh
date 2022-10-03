#!/bin/bash

sudo apt-get install python3.9 python3.9-venv

rm -r venv
python3.9 -m venv venv
venv/bin/pip install --upgrade pip && venv/bin/pip install -r requirements.txt

# enabling autocompletion - https://pypi.org/project/argcomplete/
sudo venv/bin/activate-global-python-argcomplete

THIS_FILE_DIR="$(realpath .)"
sudo ln -s "${THIS_FILE_DIR_DIR}/pine-craft.sh" /usr/bin/pine-craft