FROM python:3.9.6-alpine3.14
WORKDIR /app
COPY . .

# Install dependencies
RUN apk add --no-cache gcc libffi-dev musl-dev ffmpeg aria2 \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir --upgrade pip

# Run the application
CMD [ "python", "./main.py" ]
