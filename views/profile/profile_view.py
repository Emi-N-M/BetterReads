import flask
import flask_login
import sirope
from model.userdto import UserDto

def get_blprint():
    profile = flask.blueprints.Blueprint("profile", __name__,
    url_prefix="/profile",
    template_folder="templates",
    static_folder="static")
    syrp = sirope.Sirope()
    return profile, syrp

profile_blprint, srp = get_blprint()
@flask_login.login_required


@profile_blprint.route("/")
def profile():
    try:
        usr = UserDto.current_user()
        sust = {
            "usr":usr,
        }
        return flask.render_template("profile.html",**sust)
    except:
        return flask.redirect("/error")
