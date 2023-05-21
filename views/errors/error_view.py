import flask
import flask_login
import sirope
from model.userdto import UserDto

def get_blprint():
    error = flask.blueprints.Blueprint("error", __name__,
    url_prefix="/error",
    template_folder="templates",
    static_folder="static")
    syrp = sirope.Sirope()
    return error, syrp

error_blprint, srp = get_blprint()


@error_blprint.route("/")
def error():
    return flask.render_template("error.html")

