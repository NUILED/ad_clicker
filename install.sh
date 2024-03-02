#!bin/bash
apt install git -y
sudo apt update && sudo apt install -y libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libatspi2.0-0 libxcomposite1 libgbm1 wget gnupg ffmpeg python3-full xvfb tor

git clone https://github.com/NuIled/Google-Ads-Clicker.git

cd Google-Ads-Clicker

python3 -m venv env

source env/bin/activate

python3 -m pip install -r requirements.txt

pip install playwright

python3 -m playwright install

python3 -m playwright install-deps

sudo rm -rf /etc/tor/torrch

sudo mv torrch /etc/tor/

service tor start

xvfb-run python3 Google-Ads-Clicker.py