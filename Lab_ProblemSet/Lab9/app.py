import os
import sqlite3
from flask import g
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('birthdays.db')
    return db


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

        return redirect("/")

    else:

        # TODO: Display the entries in the database on index.html

        return render_template("index.html")
