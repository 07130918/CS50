from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

SPORTS = [
    "Dodgeball",
    "Flag Football",
    "Soccer",
    "Volleyball",
    "Ultimate Frisbee"
]


@app.route("/")
def index():
    # render_templateは値の引き渡しができる. フォームから値が送られてくる場合, get()の第2引数にデフォルト値を取れる
    # return render_template("hoge.html", name=request.form.get("name", "world"))
    return render_template("index.html", sports=SPORTS)


@app.route("/register", methods=["POST"])
def register():
    # 不正な値をガード
    # request.argsでhttpのget, .formでpost
    name = request.form.get("name")
    sport = request.form.get("sport")
    if not name:
        return render_template("error.html", message="Missing name")
    if not sport:
        return render_template("error.html", message="Missing sport")
    if sport not in SPORTS:
        return render_template("error.html", message="Invalid sport")

    return render_template("/success.html")
