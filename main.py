from flask import Flask, render_template, request, redirect, url_for
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from forms import SearchVenue
from forms import VenueInfo
import secrets
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

    step = int(request.args.get("step", 1))


    if form_search_venue.validate_on_submit():
        #store details in sessions.
        step += 1
        return redirect(url_for("add_place", step=step))
    elif form_venue_info.validate_on_submit():
        # store details in sessions.
        return redirect(url_for("home"))


    if step == 1:
        return render_template("add.html", form=form_search_venue)
    elif step == 2:
        return render_template("add_venue.html", form=form_venue_info)





@app.route("/<location>")
def show_venue(location):
    #reads db for cafes with specified location.
    cafe = db.session.execute(db.select(Cafe).where(Cafe.location == location)).scalars()
    cafes_list = cafe.all()
    # print(len(cafes_list))

    return render_template("show-venue.html", cafes_list=cafes_list, location=location)




if __name__ == "__main__":
    app.run(debug=True)
