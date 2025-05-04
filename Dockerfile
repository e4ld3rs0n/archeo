FROM python:3.11-slim

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

# Install dockerize
ADD https://github.com/jwilder/dockerize/releases/download/v0.9.3/dockerize-linux-amd64-v0.9.3.tar.gz /tmp/
RUN tar -C /usr/local/bin -xzvf /tmp/dockerize-linux-amd64-v0.9.3.tar.gz

# We use dockerize to wait for the database to be ready
# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "main:app"]
