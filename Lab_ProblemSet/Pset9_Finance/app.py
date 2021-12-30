import datetime
import os
from tempfile import mkdtemp

from flask import Flask, g, redirect, render_template, request, session
from flask_session import Session
from werkzeug.exceptions import (HTTPException, InternalServerError,
                                 default_exceptions)
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, get_db, login_required, lookup, usd

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

        # ガード
        if find_user_by(user_name, curs):
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
            curs.execute(
                'INSERT INTO users(username, hash) values(?, ?)', (user_name, hash)
            )
            # sessionに値を格納し登録後はログイン状態にし、ルートパスにリダイレクト
            session["user_id"] = find_user_by(user_name, curs)["id"]
        except Exception as e:
            print(e)
            db.rollback()
        finally:
            db.commit()

        return redirect("/")
    # HTTP GET
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
        user = find_user_by(user_name, curs)

        # Ensure username exists and password is correct
        if user is None or not check_password_hash(user["hash"], password):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = user["id"]
        return redirect("/")
    # HTTP GET
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
    stocks = call_stocks()
    if not stocks:
        return render_template("index.html", message="You don't have any stocks yet")

    # ここからhtmlに受け渡しのためのデータ加工する関数の呼び出し
    processed_stocks, cash, all_assets = call_portfolio(stocks)
    return render_template(
        "index.html", stocks=processed_stocks, cash=cash, all_assets=all_assets
    )


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        # ガード
        if not symbol:
            return render_template("quote.html", error_message='Please enter symbol')

        quote = lookup(symbol)
        if quote == 'Invaild Symbol':
            return render_template("quote.html", error_message='Invalid Symbol')
        elif quote is None:
            # 何かしらのエラーでlookupからNoneがか返ってきた時
            return render_template(
                "quote.html", error_message="Any errors have occurred."
            )

        return render_template("quote.html", quote=quote)
    # GET
    else:
        return render_template("quote.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    return order("buy")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return order("sell")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


# サポート関数群
def find_user_by(user_name, curs):
    curs.execute(f'SELECT * FROM users WHERE username="{user_name}"')
    return curs.fetchone()


def call_stocks():
    db = get_db()
    curs = db.cursor()
    curs.execute(
        'SELECT symbol, company_name as name, SUM(shares) as shares'
        f' FROM transaction_records WHERE user_id="{session["user_id"]}"'
        'GROUP BY symbol'
    )
    # 全て売り終わったあと、stock['shares']が0のものは表示しない
    return [stock for stock in curs.fetchall() if stock['shares']]


def call_portfolio(stocks):
    db = get_db()
    curs = db.cursor()
    cash = call_cash(curs)
    stocks = apend_attribute_to(stocks)
    all_assets = calculate_all_assets(stocks)
    all_assets += cash
    return stocks, cash, all_assets


def call_cash(curs):
    curs.execute(f'SELECT cash FROM users WHERE id="{session["user_id"]}"')
    return curs.fetchone()["cash"]


def apend_attribute_to(stocks):
    for stock in stocks:
        stock["current_price"] = lookup(stock["symbol"])["price"]
        stock["total"] = stock["shares"] * stock["current_price"]
    return stocks


def calculate_all_assets(stocks):
    all_assets = 0
    for stock in stocks:
        all_assets += stock["total"]
    return all_assets


def order(type):
    """Buy shares of stock or Sell shares of stock"""
    if request.method == "POST":
        shares = request.form.get("shares")
        symbol = request.form.get("symbol")
        # 正常系の行までガード節
        if not shares:
            return apology("Please enter shares")

        if type == "buy":
            quote = lookup(symbol)
            if not symbol or quote == "Invaild Symbol":
                return apology("Please enter correct symbol")
        # sell
        else:
            stocks = call_stocks()
            if not symbol:
                return apology("Please choose a company")
            for stock in stocks:
                if stock["symbol"] == symbol and float(shares) > stock["shares"]:
                    return apology("The order volume exceeds the portfolio shares")

            quote = lookup(symbol)
        if quote is None:
            # 何かしらのエラーでlookupからNoneがか返ってきた時
            return render_template("buy.html", message="Any errors have occurred.")

        # 正常系
        db = get_db()
        curs = db.cursor()
        curs.execute(f'SELECT * FROM users WHERE id="{session["user_id"]}"')
        user = curs.fetchone()
        # 計算での型はfloatで統一
        user["cash"] = float(user["cash"])
        shares = float(shares)

        if type == "buy" and user["cash"] < shares * quote["price"]:
            return render_template("buy.html", message="You don't have enough cash")

        try:
            if type == "buy":
                user["cash"] -= shares * quote["price"]
                code_shares = shares
            # sell
            else:
                code_shares = -1 * shares
                user["cash"] += shares * quote["price"]

            record = (
                session["user_id"], type, code_shares, quote["price"],
                quote["name"], quote["symbol"],
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            curs.execute(
                'INSERT INTO transaction_records(user_id, action, shares, price,'
                'company_name, symbol, transaction_datetime) values(?,?,?,?,?,?,?)',
                record
            )
            curs.execute(
                'UPDATE users SET cash=? WHERE id=?',
                (user["cash"], session["user_id"])
            )
        except Exception as e:
            print(e)
            if type == "buy":
                user["cash"] += shares * quote["price"]
            # sell
            else:
                user["cash"] -= shares * quote["price"]

            db.rollback()
        finally:
            db.commit()

        return render_template(f"{type}.html", message="The deal is done")
    # GET
    else:
        if type == "buy":
            return render_template("buy.html")
        # sell
        else:
            stocks = call_stocks()
            if not stocks:
                return render_template(
                    "index.html", message="You don't have any stocks yet"
                )

            return render_template("sell.html", stocks=stocks)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
