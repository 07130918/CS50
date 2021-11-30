from crypt import methods
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    # request.argsでhttpのget, .formでpost
    # 第2引数にデフォルト値を取れる
    # return render_template("hoge.html", name=request.form.get("name", "world"))
    return render_template("success.html")
