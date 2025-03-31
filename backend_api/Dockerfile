# Используем базовый образ Alpine
FROM alpine:latest

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости
RUN apk add --no-cache \
    python3 \
    py3-pip \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    postgresql-dev

# Копируем файлы проекта в контейнер
COPY backend_api .


# Устанавливаем зависимости с флагом --break-system-packages
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt
ENV PYTHONPATH="/app:${PYTHONPATH}"

# Команда для запуска бота
CMD ["python3", "bot/main.py"]