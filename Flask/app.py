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
    return render_template("index.html", sports=SPORTS)


@app.route("/register", methods=["POST"])
def register():
    # 不正な値をガード
    # request.argsでhttpのget, .formでpost
    if not request.form.get("name") or request.form.get("sport") not in SPORTS:
        return render_template("failure.html")
    
    # render_templateは値の引き渡しができる. get()の第2引数にデフォルト値を取れる
    # return render_template("hoge.html", name=request.form.get("name", "world"))
    return render_template("success.html")
