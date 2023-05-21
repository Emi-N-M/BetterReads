import flask
import flask_login
import sirope
from model.bookdto import BookDto
from model.reviewdto import ReviewDto
from model.userdto import UserDto
import requests

def get_blprint():
    book = flask.blueprints.Blueprint("book", __name__,
    url_prefix="/book",
    template_folder="templates",
    static_folder="static")
    syrp = sirope.Sirope()
    return book, syrp



book_blprint, srp = get_blprint()
@flask_login.login_required
@book_blprint.route("/")
def book():
    try:
        sust = api_request()
        return flask.render_template("book.html", **sust)
    except:
        return flask.redirect("/error")

@flask_login.login_required
def api_request():
    base_url = "https://www.googleapis.com/books/v1/volumes/"
    bookId = flask.request.args.get('bookId')
    req = base_url + bookId
    response = requests.get(req)

    # get book reviews
    book = srp.find_first(BookDto, lambda b: b.bookId == bookId)
    review_list = []
    usr_review = []

    # check if user has reviewed this book
    usr = UserDto.current_user()
    
    has_reviewed = bookId in usr.books_reviewed
    if book is not None:
        review_list_oids = book.oids_reviews

        for review in review_list_oids:
            r = srp.load(review)
            if r.owner_email == usr.email:
                usr_review.append(r)
            else:  
                review_list.append(r)

    book =  api_response_reader(response.json())
    if len(usr_review) != 0:
        review_list.insert(0, usr_review[0])

    print(has_reviewed)
    sust={
        "book": book,
        "reviews": review_list,
        "has_reviewed": has_reviewed,
        "usr": usr
    }

    return sust


def api_response_reader(res):
    i = res
    title =  i["volumeInfo"]["title"] if i["volumeInfo"]["title"] is not None else "None"
    imgSrc =  i["volumeInfo"]["imageLinks"]["smallThumbnail"] if "imageLinks"  in i["volumeInfo"] else "None"
    authors =  i["volumeInfo"]["authors"] if "authors"  in i["volumeInfo"] else "None"
    description =  i["volumeInfo"]["description"] if "description"  in i["volumeInfo"] else "None"
    pageCount =  i["volumeInfo"]["pageCount"] if "pageCount"  in i["volumeInfo"] else "None"
    bookId = i["id"]


    book = {"title":title,
        "imgSrc": imgSrc,
        "bookId":bookId,
        "authors":array_reader(authors),
        "description":description,
        "pageCount":pageCount
        }

    return book


def array_reader(arr:list):
    return ', '.join(arr) if arr is not None and len(arr)>1 else str(arr[0])


@book_blprint.route("/save_review", methods=["POST"])
def save_review():
    try:
        content_txt = flask.request.form.get("content")
        rating_txt = flask.request.form.get("rating")
        book_id = flask.request.form.get("bookId")

        if not content_txt or not book_id or not rating_txt:
            flask.flash("Faltan campos")
            return flask.redirect("/book/?bookId=" + book_id)


        # Update or create
        usr = UserDto.current_user()
        if book_id in usr.books_reviewed:

            review = srp.find_first(ReviewDto, lambda b: b.book_id == book_id and b.owner_email == usr.email)

            review.set_content = content_txt
            review.set_rating = rating_txt
            srp.save(review)
        
        else:
            # Save review
            rating_oid = srp.save(ReviewDto(book_id,rating_txt,content_txt, usr.name, usr.email))

            # Add review to user
            usr.add_review_oid(rating_oid)
            srp.save(usr)

            # Add review to book
            book = srp.find_first(BookDto, lambda b: b.bookId == book_id)
            print(book) 
            if book is not None:
                book.add_review_oid(rating_oid)
                srp.save(book)

            else:
                book = BookDto(book_id)
                book.add_review_oid(rating_oid)
                srp.save(book)

            usr.add_books_reviewed(book_id)
            srp.save(usr)
        
        return flask.redirect("/book/?bookId=" + book_id)
    except Exception as e:
        print(e)
        return flask.redirect("/error")
    
