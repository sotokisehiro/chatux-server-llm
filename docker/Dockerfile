FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV DEBCONF_NOWARNINGS=yes

RUN apt-get update && apt-get upgrade -y
RUN apt-get dist-upgrade -y && apt-get autoremove -y
RUN apt-get install -y git build-essential

RUN git clone https://github.com/sotokisehiro/chatux-server-llm.git /app
WORKDIR /app
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements-cpp.txt

COPY ./docker/entrypoint.sh /
RUN chmod 755 /entrypoint.sh

EXPOSE 8001
ENTRYPOINT ["/entrypoint.sh"]

