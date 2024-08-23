FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y python3-dev

WORKDIR /home/projects/serenity
ADD . /home/projects/

RUN pip install -U pip
RUN pip install -r requirements.txt --default-timeout=1000

EXPOSE 8000
