
from datetime import datetime
class ReviewDto:
    def __init__(self,book_id, rating, content, owner_name, owner_email):
        self._book_id = book_id
        self._rating = rating
        self._content = content
        self._owner_name = owner_name
        self._owner_email = owner_email
        self._time = datetime.now()

    @property
    def book_id(self):
        return self._book_id


    @property
    def rating(self):
        return self._rating

    @rating.setter
    def set_rating(self, rating):
       self._rating = rating

    @property
    def owner_name(self):
        return self._owner_name

    @property
    def owner_email(self):
        return self._owner_email

    @property
    def content(self):
        return self._content
    
    @content.setter
    def set_content(self, content):
       self._content = content 

    @property
    def time(self):
        return self._time
    
    def getTitle(self):
        return f"{self.owner_name} ha dado una valoración de: {self.rating}"

    def getContent(self):
        return f"{self.content}"