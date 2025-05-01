# Используем базовый образ Alpine
FROM python:alpine

WORKDIR /app
COPY requirements.txt requirements.txt

COPY app .

RUN pip install --no-cache-dir --break-system-packages -r requirements.txt
ENV PYTHONPATH="/app:${PYTHONPATH}"

CMD ["python3", "main.py"]