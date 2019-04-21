FROM python:3.7

RUN apt-get update
RUN apt-get install -y mdbtools

COPY app /usr/src/
WORKDIR /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED 1
RUN useradd -m appuser
USER appuser
CMD ["/usr/local/bin/gunicorn", "--workers=2", "--bind=0.0.0.0:$PORT", "dump_mdb.app:application"]
