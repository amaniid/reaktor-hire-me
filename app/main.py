import json
from flask import Flask, redirect, url_for, render_template
from .read_status import readstatusfile


app = Flask(__name__)


@app.before_first_request
def get_data():
    global pkgs
    pkgs = readstatusfile()
    # pkgs = map(json.dumps, pkgs)


@app.route("/")
def home():
    return render_template("index.html", mydata=pkgs)


@app.route("/cv")
def cv():
    return render_template("cv.html")


@app.route("/cover-letter")
def cover_letter():
    return render_template("cover-letter.html")


@app.route('/package/' + b'<pkgname>'.decode('utf-8'), methods=['GET'])
def package(pkgname):
    if pkgname in pkgs[0]:
        pkg_index = pkgs[0].index(pkgname)
        return render_template("packagepage.html", name=pkgname, depends=pkgs[1][pkg_index], description=pkgs[2][pkg_index])
    else:
        return render_template("404.html")


if __name__ == "__main__":
    app.run(debug=True)
