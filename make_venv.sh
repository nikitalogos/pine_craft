#!/bin/bash

sudo apt-get install python3.9 python3.9-venv

rm -r venv
python3.9 -m venv venv
venv/bin/pip install --upgrade pip && venv/bin/pip install -r requirements.txt

sudo venv/bin/activate-global-python-argcomplete