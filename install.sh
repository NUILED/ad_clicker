#!bin/bash

apt install -y python3
apt install -y pip

pip install playwright
python3 -m playwright install
python3 -m playwright install-deps

xvfb-run python3 Google-Ads-Clicker.py
