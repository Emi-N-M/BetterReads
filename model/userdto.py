import sirope
import flask_login
import werkzeug.security as safe

class UserDto(flask_login.UserMixin):
    def __init__(self, email, password, name):
        self._name = name
        self._email = email
        self._password = safe.generate_password_hash(password)
        self._reviews_oids = []
        self._books_reviewed = []

    @property
    def email(self):
        return self._email
    
    @property
    def name(self):
        return self._name

    @property
    def oids_reviews(self):
        if not self.__dict__.get("_reviews_oids"):
            self._reviews_oids = []

        return self._reviews_oids


    @property
    def books_reviewed(self):
        if not self.__dict__.get("_books_reviewed"):
            self._books_reviewed = []

        return self._books_reviewed

    def add_review_oid(self, review_oid):
        self.oids_reviews.append(review_oid)


    def add_books_reviewed(self, bookId):
        self.books_reviewed.append(bookId)
    
    def get_id(self):
        return self.email
    
    def chk_password(self, pswd):
        return safe.check_password_hash(self._password, pswd)
    
    @staticmethod
    def current_user():
        usr = flask_login.current_user
        if usr.is_anonymous:
            flask_login.logout_user()
            usr = None
        return usr
    
    @staticmethod
    def find(s: sirope.Sirope, email: str) -> "UserDto":
        return s.find_first(UserDto, lambda u: u.email == email)