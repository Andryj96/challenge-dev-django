FROM python:3.10

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /code
COPY requeriments.txt /code/

RUN pip install -r requeriments.txt

COPY . /code/
