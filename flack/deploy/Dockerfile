FROM python:3.6-stretch

RUN mkdir /code
WORKDIR /code

COPY . /code/
RUN apt-get -qq update
RUN pip install -r requirements.txt
RUN pip install celery[redis]
RUN pip install -e .

EXPOSE 5000