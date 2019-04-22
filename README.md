dump_mdb
========

A microservice that dumps a table of an MDB file as CSV

Build and run with:

    $ docker build --tag=dumpmdb:latest .
    $ docker run -p 8000:8000 \
        -e PORT=8000 \
        -e BASIC_USERNAME=user \
        -e BASIC_PASSWORD=pass \
        dumpmdb:latest

`curl` client example:

    $ curl -v -u user:pass \
        -F "table_name=users" \
        -F "mdb_file=@database.mdb" \
        http://localhost:8000/

Python `requests` client example:

    >>> response = requests.post(
    ...     'http://localhost:8000/',
    ...     auth=('user', 'pass'),
    ...     data={'table_name': table_name},
    ...     files={'mdb_file': open(mdb_filename, 'rb')},
    ... )
