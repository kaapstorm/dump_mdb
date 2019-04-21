dump_mdb
========

A microservice that dumps a table of an MDB file as CSV

Build and run with:

    $ docker build --tag=dumpmdb:latest .
    $ docker run -p 8000:8000 -e PORT=8000 dumpmdb:latest
