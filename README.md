dump_mdb
========

A microservice that dumps a table of an MDB file as CSV

Build and run with:

    $ docker build --tag=dumpmdb:latest .
    $ docker run -p 8000:8000 \
        -e PORT=8000 \
        -e MDB_DUMP_USERNAME=user123 \
        -e MDB_DUMP_PASSWORD=pass456 \
        dumpmdb:latest

`curl` client example:

    $ curl -v -u user123:pass456 \
        -F "table_name=users" \
        -F "mdb_file=@database.mdb" \
        http://localhost:8000/

Python `requests` client example:

    >>> response = requests.post(
    ...     'http://localhost:8000/',
    ...     auth=('user123', 'pass456'),
    ...     data={'table_name': 'users'},
    ...     files={'mdb_file': open('database.mdb', 'rb')},
    ... )
