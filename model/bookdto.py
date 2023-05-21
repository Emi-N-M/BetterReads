
from datetime import datetime
class BookDto:
    def __init__(self, bookId):
        self._bookId= bookId
        self._reviews_oids = []


        
    @property
    def bookId(self):
        return self._bookId


    def add_review_oid(self, review_oid):
        self.oids_reviews.append(review_oid)

    @property
    def oids_reviews(self):
        if not self.__dict__.get("_reviews_oids"):
            self._reviews_oids = []

        return self._reviews_oids