import flask
import flask_login
import sirope
from model.userdto import UserDto
import requests

def get_blprint():
    search = flask.blueprints.Blueprint("search", __name__,
    url_prefix="/search",
    template_folder="templates",
    static_folder="static")
    syrp = sirope.Sirope()
    return search, syrp

search_blprint, srp = get_blprint()
@flask_login.login_required


@search_blprint.route("/")
def search():
    return flask.send_from_directory(search_blprint.static_folder, "search.html")

@flask_login.login_required
@search_blprint.route("/", methods=["POST"])
def api_request():
    try:
        base_url = "https://www.googleapis.com/books/v1/volumes?"
        query = flask.request.form.get("query")
        req = base_url + "q=" + query.replace(" ","+") + "&maxResults=40"
        print(req)
        response = requests.get(req)

        books =  api_response_reader(response.json())
        sust={
            "books": books
        }

        return flask.render_template("results.html",**sust)
    except:
        return flask.redirect("/error")



def api_response_reader(res):
    items = res["items"]
    books = list()
    n=0
    for i in items:
        title =  i["volumeInfo"]["title"] if i["volumeInfo"]["title"] is not None else "None"
        imgSrc =  i["volumeInfo"]["imageLinks"]["smallThumbnail"] if "imageLinks"  in i["volumeInfo"] else "None"
        bookId = i["id"]



        books.append({"title":title,
            "imgSrc": imgSrc,
            "bookId":bookId
            })
        
        
        #books[n]["title"] = i["volumeInfo"]["title"]
        n+=1
    #books["total_books"] = n
    return books