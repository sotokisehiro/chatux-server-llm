FROM ubuntu:23.04

ENV DEBIAN_FRONTEND=noninteractive
ENV DEBCONF_NOWARNINGS=yes

RUN apt-get update && apt-get upgrade -y
RUN apt-get dist-upgrade -y && apt-get autoremove -y
RUN apt-get install -y git build-essential
RUN apt-get install -y python3 python3-venv

RUN git clone https://github.com/sotokisehiro/chatux-server-llm.git /app
WORKDIR /app
RUN python3 -m venv /venv
RUN . /venv/bin/activate && python -m pip install --upgrade pip
RUN . /venv/bin/activate && python -m pip install -r requirements.txt

COPY ./docker/entrypoint.sh /
RUN chmod 755 /entrypoint.sh

EXPOSE 8001
ENTRYPOINT ["/entrypoint.sh"]

