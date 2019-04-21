FROM python:3.7

RUN apt-get update
RUN apt-get install -y mdbtools

COPY ./dump_mdb /usr/src/dump_mdb
WORKDIR /usr/src/dump_mdb/
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED 1
RUN useradd -m appuser
USER appuser
CMD gunicorn --bind=0.0.0.0:$PORT app:app
