import os
from contextlib import closing
from functools import wraps
from subprocess import check_output, CalledProcessError
from tempfile import NamedTemporaryFile

from flask import Flask, render_template, Response, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, FileField
from wtforms.validators import DataRequired

MDB_EXPORT_CMD = '/usr/bin/mdb-export'
MDB_TABLES_CMD = '/usr/bin/mdb-tables'
MDB_DUMP_USERNAME = os.environ['MDB_DUMP_USERNAME']
MDB_DUMP_PASSWORD = os.environ['MDB_DUMP_PASSWORD']


app = Flask(__name__)
app.config.from_mapping(WTF_CSRF_ENABLED=False)


class MdbTableForm(FlaskForm):
    mdb_file = FileField('MDB file', validators=[FileRequired()])
    table_name = StringField('Table name', validators=[DataRequired()])


def check_auth(username, password):
    return username == MDB_DUMP_USERNAME and password == MDB_DUMP_PASSWORD


def unauthorized_response():
    return Response(
        'Unauthorized', 401,
        headers={'WWW-Authenticate': 'Basic realm="Login required"'}
    )


def ok_response():
    return Response('OK', 200)


def authenticate(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return ok_response()
        if not check_auth(auth.username, auth.password):
            return unauthorized_response()
        return func(*args, **kwargs)
    return decorated


@app.route("/", methods=['GET', 'POST'])
@authenticate
def index():
    form = MdbTableForm()
    if form.validate_on_submit():
        try:
            csv_export = export_table(
                form.mdb_file.data,
                str(form.table_name.data)
            )
            return Response(csv_export, 200, mimetype='text/csv')
        except CalledProcessError:
            return Response(
                "That didn't work. Please check the file is valid.", 400
            )
        except ValueError:
            return Response(
                "That didn't work. Please check the table exists.", 400
            )
    return render_template('mdb_table_form.html', form=form)


def export_table(mdb_file, table):
    with closing(NamedTemporaryFile()) as tmp_file:
        mdb_file.save(tmp_file)
        tables = check_output((MDB_TABLES_CMD, '-1', tmp_file.name))
        tables = [n for n in tables.decode('ascii').split('\n') if n]
        if table not in tables:
            raise ValueError('Table not found in MDB')
        csv_export = check_output(
            (MDB_EXPORT_CMD, tmp_file.name, table)
        )
    return csv_export


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ['PORT'])
