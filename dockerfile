# Используем базовый образ Linux Alpine
FROM alpine:latest

# Устанавливаем необходимые пакеты
RUN apk --no-cache add \
    python3 \
    py3-pip \
    bash \
    tzdata \
    git \
    pip3 install --upgrade pip \
    pip3 install requests pyodbc schedule

# Клонируем репозиторий из GitHub
RUN git clone https://github.com/serty2005/MHrepo.git /opt/app

# Создаем файл крона
RUN echo "20 4 * * * root /usr/bin/python3 /opt/app/getfomsd.py" > /etc/cron.d/mycronjob
RUN echo "21 4 * * * root /usr/bin/python3 /opt/app/getfromjson.py" > /etc/cron.d/mycronjob
RUN echo "22 4 * * * root /usr/bin/python3 /opt/app/pushchangestosd.py" > /etc/cron.d/mycronjob

# Запускаем crond при запуске контейнера
CMD ["crond", "-f"]
