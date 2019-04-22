import os
from contextlib import closing
from subprocess import check_output, CalledProcessError
from tempfile import NamedTemporaryFile

from flask import Flask, render_template, Response
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, FileField
from wtforms.validators import DataRequired

MDB_EXPORT_CMD = '/usr/bin/mdb-export'


app = Flask(__name__)
app.config.from_mapping(WTF_CSRF_ENABLED=False)


class MdbTableForm(FlaskForm):
    mdb_file = FileField('MDB file', validators=[FileRequired()])
    table_name = StringField('Table name', validators=[DataRequired()])


@app.route("/", methods=['GET', 'POST'])
def index():
    form = MdbTableForm()
    if form.validate_on_submit():
        try:
            response = dump_table(form.mdb_file, form.table_name)
            mimetype = 'text/csv'
        except CalledProcessError:
            response = ("That didn't work. "
                        "Please check the file is valid and the table exists")
            mimetype = 'text/plain'
        return Response(response, 200, mimetype=mimetype)
    return render_template('mdb_table_form.html', form=form)


def dump_table(mdb_file, table_name):
    table_name = str(table_name.data)
    with closing(NamedTemporaryFile()) as tmp_file:
        mdb_file.data.save(tmp_file)
        output = check_output(
            (MDB_EXPORT_CMD, tmp_file.name, table_name)
        )
    return output


if __name__ == "__main__":
    app.run(host='0.0.0.0')
