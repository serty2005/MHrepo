# Используем базовый образ Linux Alpine
FROM alpine:latest

# Устанавливаем необходимые пакеты
RUN apk --no-cache add \
    python3 \
    py3-pip \
    bash \
    tzdata \
    git \
    && pip3 install --upgrade pip --break-system-packages\
    && pip3 install --break-system-packages requests schedule

# Удаляем файл EXTERNALLY-MANAGED
#RUN rm /usr/lib/python3.11/EXTERNALLY-MANAGED

ENV TZ=Europe/Moscow

# Клонируем репозиторий из GitHub
RUN git clone https://github.com/serty2005/MHrepo.git /opt/app

# Создаем файл крона
RUN echo "20 4 * * * root /usr/bin/python3 /opt/app/getfomsd.py > /dev/stdout" > /etc/periodic/daily/mycronjob
RUN echo "21 4 * * * root /usr/bin/python3 /opt/app/getfromjson.py > /dev/stdout" >> /etc/periodic/daily/mycronjob
RUN echo "22 4 * * * root /usr/bin/python3 /opt/app/pushchangestosd.py > /dev/stdout" >> /etc/periodic/daily/mycronjob

# Запускаем crond при запуске контейнера
CMD ["crond", "-f"]
