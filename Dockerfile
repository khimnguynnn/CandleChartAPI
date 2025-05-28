# syntax=docker/dockerfile:1
FROM python:3.10-slim

WORKDIR /app

COPY main.py ./
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["python", "main.py"] 