# Используем базовый образ Linux Alpine
FROM alpine:latest

# Устанавливаем необходимые пакеты
RUN apk --no-cache add \
    python3 \
    py3-pip \
    bash \
    tzdata \
    git \
    && pip3 install --upgrade pip \
    && pip3 install requests pyodbc schedule

# Устанавливаем переменные окружения
ENV BDPATH=/path/to/bd \
    JSONPATH=/path/to/json \
    MSSQLSTRING=your_mssql_string \
    SDKEY=your_sd_key

# Клонируем репозиторий из GitHub
RUN git clone https://github.com/serty2005/MHrepo.git /app

# Создаем файл крона
RUN echo "20 4 * * * root /usr/bin/python3 /app/script1.py && /usr/bin/python3 /app/script2.py" > /etc/cron.d/mycronjob

# Запускаем crond при запуске контейнера
CMD ["crond", "-f"]
