FROM python:3.12.3
WORKDIR /app
COPY . .
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN python serverV3.py
CMD gunicorn app:app & python3 main.py
