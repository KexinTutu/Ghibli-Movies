FROM python:3
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/

RUN pip install --no-cache-dir --default-timeout=100 future -r requirements.txt

COPY . /code/