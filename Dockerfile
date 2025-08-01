FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && \
    apt-get install -y ffmpeg jq python3-dev && \
    rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python3 -m pip check yt-dlp
CMD gunicorn app:app & python3 main.py

FROM python:3.10.8-slim-buster
RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends gcc libffi-dev musl-dev ffmpeg aria2 python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/
WORKDIR /app/
RUN pip3 install --no-cache-dir --upgrade --requirement requirements.txt
RUN pip install pytube
ENV COOKIES_FILE_PATH="youtube_cookies.txt"
CMD gunicorn app:app & python3 main.py
