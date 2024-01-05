FROM python:3.10-slim-buster

# Set the working directory to /src
WORKDIR /src
# install required packages

RUN apt-get update && apt-get install -y libnss3 \
                libnspr4 \
                libatk1.0-0 \
                libatk-bridge2.0-0 \
                libcups2 \
                libatspi2.0-0 \
                libxcomposite1 \
                libgbm1 \ 
                wget \
                gnupg \
                ffmpeg

RUN rm -rf /var/lib/apt/lists/*

# upgrade pip
RUN python -m pip install --no-cache-dir --upgrade pip

# install dependencies
COPY ./requirements.txt pythonapp.py script.sh /src
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the image
COPY . /src

# set display port to avoid crash
ENV DISPLAY=:99
RUN chmod +x /src/script.sh
# Start Xvfb
CMD Xvfb :99 -screen 0 1920x1080x16

ENTRYPOINT ["./script.sh"]

