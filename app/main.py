from flask import Flask, redirect, url_for, render_template
import .read_status


app = Flask(__name__)


@app.before_first_request
def get_data():
    global pkgs
    pkgs = read_status.readstatusfile()


@app.route("/")
def home():
    return render_template("404.html")
    # return render_template("homepage.html", content=pkgs)

@app.route('/package/' + b'<pkgname>'.decode('utf-8'), methods=['GET'])
def package(pkgname):
    if pkgname in pkgs[0]:
        pkg_index = pkgs[0].index(pkgname)
        return render_template("packagepage.html", name=pkgname, depends=pkgs[1][pkg_index], description=pkgs[2][pkg_index])
    else:
        return render_template("404.html")


if __name__ == "__main__":
    app.run(debug=True)
