import sqlite3

from flask import (Flask, flash, g, jsonify, redirect, render_template,
                   request, session)

# Configure application
app = Flask(__name__)


# https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/patterns/sqlite3.html
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('birthdays.db')
        db.row_factory = dict_factory
    return db


def dict_factory(cursor, row):
    """
        取得レコードをtuple型からdict型に変換
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.teardown_appcontext
def close_connection(exception):
    """
        @app.teardown_appcontextでアプリ開始時にDB接続,終了時にDB接続を切る
    """
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/", methods=["GET", "POST"])
def index():
    db = get_db()
    curs = db.cursor()
    if request.method == "POST":

        # TODO: Add the user's entry into the database
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")
        # ガードを作る必要あり
        curs.execute(
            'INSERT INTO birthdays(name, month, day)'
            f'values("{name}", "{month}", "{day}")'
        )
        db.commit()
        return redirect("/")

    # HTTP GET
    else:

        # TODO: Display the entries in the database on index.html
        curs.execute('SELECT * FROM birthdays')
        persons = curs.fetchall()
        return render_template("index.html", persons=persons)
