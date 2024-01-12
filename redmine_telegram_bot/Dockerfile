FROM python:3.7-slim

WORKDIR /app

RUN apt-get update  \
    && apt-get install -y gcc  \
    && apt install netcat-traditional

COPY requirements.txt /app

RUN pip install --upgrade pip  \
    && pip install -r ./requirements.txt --no-cache-dir

COPY . ./

RUN chmod +x ./server-entrypoint.sh
RUN chmod +x ./worker-entrypoint.sh
RUN chmod +x ./beat-entrypoint.sh
