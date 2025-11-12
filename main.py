from flask import Flask, render_template, request, redirect, url_for, session
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from forms import SearchVenue
from forms import VenueInfo
import secrets
import os
# from flask_bootstrap import Bootstrap5





app = Flask(__name__)
key = secrets.token_hex(16)
app.secret_key = key

#INITIALIZE THE EXTENSION
# create DB object
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

#CONFIGURE THE EXTENSION: Connect extension to flask app

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"

db.init_app(app)


#Cache setup
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app, config={'CACHE_TYPE': 'SimpleCache'})

#  DEFINE MODEL

class Cafe(db.Model):
    __tablename__ = "cafe"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=False)



with app.app_context():
    db.create_all()



GOOGLE_PLACES_API_KEY = os.environ.get("API")








# VARIABLES





@app.route("/")
@cache.cached(timeout=50)
def home():
    #Reads DB and stores location in list, conditional statement ensures there is no repetition of location
    cafe = db.session.execute(db.select(Cafe).order_by(Cafe.id)).scalars()
    cafes = cafe.all()
    location_list = []
    for items in cafes:
        location = items.location
        if location not in location_list:
            location_list.append(location)


    return render_template("index.html", location_list=location_list)


@app.route("/add", methods=["GET", "POST"])
def add_place():
    form_search_venue = SearchVenue()
    form_venue_info = VenueInfo()

    #Sets session["step"] only when session[step] doesn't exist

    # if "step" not in session:
    #     session["step"] = 1

    step = session.get("step", 1)

    if request.method == "POST" and step == 1:

        #store details in sessions.

        # form_venue_info.name.data = location_name
        session["location_name"] = form_search_venue.location.data
        session["picture_url"] = form_search_venue.photo.data
        session["country"] = form_search_venue.country.data
        session["city"] = form_search_venue.city.data
        session["street_name"] = form_search_venue.street_one.data
        session["step"] = 2


        print("form one submitted")

        return redirect(url_for("add_place"))
    elif request.method == "POST" and step == 2:
        print("step 2 done form submitted")

        # store details in sessions.

        #then clear session
        return redirect(url_for("home"))


    if step == 1:
        return render_template("add.html", form=form_search_venue, api_key=GOOGLE_PLACES_API_KEY)
    elif session["step"] == 2:
        print(step)
        location_name = session.get("location_name", "")
        street_name = session.get("street_name", "")
        return render_template("add_venue.html", form=form_venue_info, name_of_venue=location_name, street=street_name, step=step)





@app.route("/<location>")
def show_venue(location):
    #reads db for cafes with specified location.
    cafe = db.session.execute(db.select(Cafe).where(Cafe.location == location)).scalars()
    cafes_list = cafe.all()
    # print(len(cafes_list))

    return render_template("show-venue.html", cafes_list=cafes_list, location=location)


# @app.route("/review")
# def review_venue_info():
#
#
#     return




if __name__ == "__main__":
    app.run(debug=True)
