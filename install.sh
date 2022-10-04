#!/bin/bash

echo "~~~~~~~~~~~~~~~Installing python3.9~~~~~~~~~~~~~~~"
sudo apt-get install python3.9 python3.9-venv

echo "~~~~~~~~~~~~~~~Creating python3 virtual environment~~~~~~~~~~~~~~~"
rm -r venv
python3.9 -m venv venv
venv/bin/pip install --upgrade pip && venv/bin/pip install -r requirements.txt

echo "~~~~~~~~~~~~~~~Enabling autocompletion - https://pypi.org/project/argcomplete/ ~~~~~~~~~~~~~~~"
sudo venv/bin/activate-global-python-argcomplete

EXE="/usr/bin/pine-craft"

echo "~~~~~~~~~~~~~~~Creating executable '${EXE}'~~~~~~~~~~~~~~~"
echo "#!/bin/bash
# PYTHON_ARGCOMPLETE_OK
$(realpath .)/venv/bin/python $(realpath .)/pine-craft.py \"\$@\"" | sudo tee ${EXE}
sudo chmod a+x ${EXE}
echo "~~~~~~~~~~~~~~~Done!~~~~~~~~~~~~~~~"