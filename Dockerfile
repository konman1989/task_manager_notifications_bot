FROM python:3.8

RUN mkdir /t_m_notifications_bot
COPY . /t_m_notifications_bot
WORKDIR /t_m_notifications_bot

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
RUN pip install --upgrade pip
COPY requirements.txt t_m_notifications_bot/requirements.txt
RUN pip install -r requirements.txt

ENTRYPOINT ["docker-entrypoint.sh"]