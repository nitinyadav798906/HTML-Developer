FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && apt-get upgrade -y \
    apt-get install -y ffmpeg jq python3-dev && \
    && apt-get clean \
    rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /app/
RUN python3 -m pip check yt-dlp
ENV COOKIES_FILE_PATH="youtube_cookies.txt"
CMD gunicorn app:app & python3 main.py
