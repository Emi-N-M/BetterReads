import flask
import sirope
import flask_login
from model.userdto import UserDto
import views.search.search_view as search_view
import views.profile.profile_view as profile_view
import views.books.books_view as books_view
import views.errors.error_view as error_view




def create_app():
    lmanager = flask_login.login_manager.LoginManager()
    fapp = flask.Flask(__name__,instance_relative_config=True)
    sirp = sirope.Sirope()
    lmanager.init_app(fapp)

    fapp.config.from_json("config.json")
    fapp.register_blueprint(search_view.search_blprint)
    fapp.register_blueprint(profile_view.profile_blprint)
    fapp.register_blueprint(books_view.book_blprint)
    fapp.register_blueprint(error_view.error_blprint)
    return fapp, lmanager, sirp


app,lm, sirp = create_app()

@lm.user_loader
def user_loader(email):
    return UserDto.find(sirp,email)

@lm.unauthorized_handler
def unauthorized_handler():
    flask.flash("Unautorized")
    
    return flask.redirect("/login")

@app.route("/")
def default_route():
    usr = UserDto.current_user()
    if usr == None:
        return flask.redirect("/login")
    
    return flask.redirect("/home")
    



@app.route("/home")
def index():
    try:
        usr = UserDto.current_user()
        
        if usr == None:
            return flask.redirect("/login")

        
        return flask.render_template("home.html")
    except:
        return flask.redirect("/error")


@app.route("/login")
def login():
    return flask.render_template("login.html")

@app.route("/register")
def register():
    return flask.render_template("register.html")


@app.route("/login",  methods=["POST"])
def loginPost():
    try:
        email_txt = flask.request.form.get("email")
        password_txt = flask.request.form.get("password")

        usr = UserDto.find(sirp, email_txt)
        print("usr: ", usr)
        if not usr:
            print("Email not registered")
            flask.flash("Email not registered",category='error')
            return flask.redirect("/login")

        elif not usr.chk_password(password_txt):
            print("Passwords do not match")
            flask.flash("Passwords do not match")
            return flask.redirect("/login")

        flask_login.login_user(usr)
        return flask.redirect("/home")
    except:
        return flask.redirect("/error")

@app.route("/register",  methods=["POST"])
def registerPost():
    try:
        email_txt = flask.request.form.get("email")
        name_txt = flask.request.form.get("name")
        password_txt = flask.request.form.get("password")
        password_confirm = flask.request.form.get("confirm_password")

        if password_txt != password_confirm:
            print("Passwords dont match")
            flask.flash("Las contraseñas no coinciden",category='error')
            return flask.redirect("/register")


        usr = UserDto.find(sirp, email_txt)
        if not usr:
            usr = UserDto(email_txt, password_txt,name_txt)
            sirp.save(usr)
            flask_login.login_user(usr)
            flask.flash("Bienvenido!",category='info')
            return flask.redirect("/home")

        else:
            print("Email already registered")
            flask.flash("Ese email ya tiene una cuenta registrada",category='error')
            return flask.redirect("/register")
    except:
        return flask.redirect("/error")

@app.errorhandler(404)
def not_found(e):
  return flask.redirect("/error")



@app.route('/logout')
def logout():
    flask_login.logout_user()
    flask.flash("User logged out")
    return flask.redirect("/")

if __name__ == '__main__':
    app.run()

