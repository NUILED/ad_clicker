FROM python:3.10-slim-buster

# Set the working directory to /src
WORKDIR /GCADS
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
                ffmpeg \
                python3 \
                pip \
                tor 

# upgrade pip
RUN python -m pip install --no-cache-dir --upgrade pip

# Copy the current directory contents into the image
COPY ./* /GCADS

RUN python -m venv env

RUN source env/bin/activate

RUN python -m pip install -r requirements.txt
# set display port to avoid crash
ENV DISPLAY=:99

RUN chmod +x /src/script.sh

# Start Xvfb
CMD Xvfb :99 -screen 0 1920x1080x16

ENTRYPOINT ["./install.sh"]