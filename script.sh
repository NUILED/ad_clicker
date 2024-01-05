#!/bin/bash

python3 -m venv myenv
source myenv/bin/activate
apt install ffmpeg
python3 -m pip install --no-cache-dir -r requirements.txt
python3 -m playwright install
python3 -m playwright install-deps
echo "RUNING SCRIPT"
python3 pythonapp.py