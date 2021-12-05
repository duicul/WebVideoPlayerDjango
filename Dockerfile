#Download Python from DockerHub and use it
FROM python:3.9-slim-buster as BASE

WORKDIR /home

ARG USER=root
USER $USER

RUN apt-get update && \
    apt-get -y install gcc mono-mcs && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY ./WebVideoPlayer .

COPY entrypoint.sh .

COPY djangoWebPlayer.ini .

EXPOSE 7700

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]