import os
import datetime
import sqlite3

from flask import Flask, g, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Make sure API key is set(環境変数からAPI_KEYの確認)
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


# https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/patterns/sqlite3.html
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('finance.db')
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


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        db = get_db()
        curs = db.cursor()

        user_name = request.form.get("username")
        password = request.form.get("password")
        password_again = request.form.get("password-again")

        curs.execute(f'SELECT * FROM users WHERE username="{user_name}"')
        user = curs.fetchone()
        if user:
            return apology("Username already exists", 403)
        elif not user_name:
            return apology("must provide username", 403)
        elif not password:
            return apology("must provide password", 403)
        elif not password_again:
            return apology("must provide password(again)", 403)
        elif password != password_again:
            return apology("Password and confirmation password are different.", 403)

        try:
            # passwordを直でdatabaseに保存しない
            hash = generate_password_hash(password)
            curs.execute("INSERT INTO users(username, hash) values(?, ?)", (user_name, hash))
            curs.execute(f'SELECT * FROM users WHERE username="{user_name}"')
            user = curs.fetchone()
        except Exception as e:
            print(e)
            db.rollback()
        finally:
            db.commit()

        # sessionに値を格納し登録後はログイン状態にし、ルートパスにリダイレクト
        session["user_id"] = user["id"]
        return redirect("/")
    # GET
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        user_name = request.form.get("username")
        password = request.form.get("password")
        # Ensure username was submitted
        if not user_name:
            return apology("must provide username", 403)
        elif not password:
            return apology("must provide password", 403)

        # Query database for username
        db = get_db()
        curs = db.cursor()
        curs.execute(f'SELECT * FROM users WHERE username="{user_name}"')
        users = curs.fetchall()

        # Ensure username exists and password is correct
        if len(users) != 1 or not check_password_hash(users[0]["hash"], password):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = users[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    return redirect("/")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    return apology("TODO")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return render_template("quote.html", error_message='Please enter symbol')

        quote = lookup(symbol)
        if type(quote) is dict:
            # jsonをきちんと取得できた時
            return render_template("quote.html", quote=quote)
        elif quote == 'Invaild Symbol':
            return render_template("quote.html", error_message='Invalid Symbol')
        else:
            # 何かしらのエラーでlookupからNoneがか返ってきた時
            return render_template("quote.html", error_message="Any errors have occurred.")
    # GET
    else:
        return render_template("quote.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # if request.method == "POST":
    #     shares = request.form.get("shares")
    #     symbol = request.form.get("symbol")
    #     if not symbol:
    #         return render_template("buy.html", error_message='Please enter symbol')
    #     elif not shares:
    #         return render_template("buy.html", error_message='Please enter shares')

    #     quote = lookup(symbol)
    #     print(quote)
    #     if type(quote) is dict:
    #         # jsonをきちんと取得できた時
    #         db = get_db()
    #         curs = db.cursor()
    #         curs.execute(f'SELECT * FROM users WHERE id = "{session["user_id"]}"')
    #         user = curs.fetchone()
    #         user["cash"] = float(user["cash"])

    #         if user["cash"] < shares * quote["price"]:
    #             return render_template("buy.html", error_message="You don't have enough cash")

    #         user["cash"] -= shares * quote["price"]
    #         try:
    #             dt_now = datetime.datetime.now()
    #             record = (session["user_id"], "buy", quote["name"], quote["symbol"], quote["price"], dt_now)

    #             curs.execute('INSERT INTO transaction_records(user_id, action, company_name, symbol, price, transaction_datetime) values(?,?,?,?,?,?)', record)
    #             curs.execute(f'UPDATE users SET cash = ? WHERE id = "{session["user_id"]}"', (user["cash"]))
    #         except Exception as e:
    #             print(e)
    #             user["cash"] += shares * quote["price"]
    #             db.rollback()
    #         finally:
    #             db.commit()

    #         return render_template("buy.html")
    #     elif quote == 'Invaild Symbol':
    #         return render_template("buy.html", error_message='Invalid Symbol')
    #     else:
    #         # 何かしらのエラーでlookupからNoneがか返ってきた時
    #         return render_template("buy.html", error_message="Any errors have occurred.")
    # # GET
    # else:
    #     return render_template("buy.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
