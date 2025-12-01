from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, Float, ForeignKey
from forms import SearchVenue
from forms import VenueInfo
import secrets
import os
import re
from typing import List
from reviewquestions import survey_data

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
    # map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    city: Mapped[str] = mapped_column(String(250), nullable=False)
    address: Mapped[str] = mapped_column(String(250), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    country: Mapped[str] = mapped_column(String(250), nullable=False)
    user_review: Mapped["Review"] = relationship(back_populates="input_restaurant")

    # has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    # has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    # has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    # can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    # seats: Mapped[str] = mapped_column(String(250), nullable=False)
    # coffee_price: Mapped[str] = mapped_column(String(250), nullable=False)



class Review(db.Model):
    __tablename__ = "review"
    id: Mapped[int] = mapped_column(primary_key=True)
    wifi: Mapped[str] = mapped_column(String(250), nullable=False)
    power_sockets: Mapped[str] = mapped_column(String(250), nullable=False)
    length_of_work: Mapped[str] = mapped_column(String(250), nullable=False)
    tables_and_chairs: Mapped[str] = mapped_column(String(250), nullable=False)
    is_it_quiet: Mapped[str] = mapped_column(String(250), nullable=False)
    audio_and_video: Mapped[str] = mapped_column(String(250), nullable=False)

    other_people_working: Mapped[str] = mapped_column(String(250), nullable=False)
    group_tables: Mapped[str] = mapped_column(String(250), nullable=False)

    coffee_available: Mapped[str] = mapped_column(String(250), nullable=False)
    food_offered: Mapped[str] = mapped_column(String(250), nullable=False)
    veggie_options: Mapped[str] = mapped_column(String(250), nullable=False)
    alcohol_offered: Mapped[str] = mapped_column(String(250), nullable=False)
    credit_cards: Mapped[str] = mapped_column(String(250), nullable=False)

    natural_light: Mapped[str] = mapped_column(String(250), nullable=False)
    outdoor_area: Mapped[str] = mapped_column(String(250), nullable=False)
    how_large: Mapped[str] = mapped_column(String(250), nullable=False)
    restroom: Mapped[str] = mapped_column(String(250), nullable=False)
    wheelchair_accessible: Mapped[str] = mapped_column(String(250), nullable=False)
    air_conditioned: Mapped[str] = mapped_column(String(250), nullable=False)
    smoke_free: Mapped[str] = mapped_column(String(250), nullable=False)
    pet_friendly: Mapped[str] = mapped_column(String(250), nullable=False)
    parking_space: Mapped[str] = mapped_column(String(250), nullable=False)

    summary: Mapped[str] = mapped_column(String(250), nullable=False)


    restaurant_id: Mapped[int] = mapped_column(ForeignKey("cafe.id"))
    input_restaurant: Mapped["Cafe"] = relationship(back_populates="user_review")




with app.app_context():
    db.create_all()



GOOGLE_PLACES_API_KEY = os.environ.get("API")



def slugify(text):
    stringed_text = str(text)
    text = stringed_text.replace(" ", "-")

    return text

def de_slugify(slugified_text):
    normalised_text = str(slugified_text).replace("-", " ")

    return normalised_text





# VARIABLES
@app.route("/api/restaurants")
def get_list_of_places():
    list_of_places = []
    with app.app_context():
        restaurants = db.session.execute(db.select(Cafe).order_by(Cafe.id)).scalars().all()

    for restaurant in restaurants:
        print(type(restaurant.name))
        list_of_places.append(restaurant.name)

    return list_of_places







@app.route("/")
@cache.cached(timeout=50)
def home():
    #Reads DB and stores location in list, conditional statement ensures there is no repetition of location
    cafe = db.session.execute(db.select(Cafe).order_by(Cafe.id)).scalars()

    cafes = cafe.all()

    location_list = []
    for items in cafes:
        location = items.city
        #TO AVOID REPETITION OF LOCATION
        if location not in location_list:
            location_list.append(location)


    return render_template("index.html", location_list=location_list)


@app.route("/add", methods=["GET", "POST"])
def add_place():
    form_search_venue = SearchVenue()
    form_venue_info = VenueInfo()



    # if "step" not in session:
    #     session["step"] = 1
    # SET STEP = 1 IF STEP IS NOT IN SESSION
    step = session.get("step", 1)

    if request.method == "POST" and step == 1:

        #store details in sessions.
        session["location_name"] = form_search_venue.location.data
        session["picture_url"] = form_search_venue.photo.data
        session["country"] = form_search_venue.country.data
        session["city"] = form_search_venue.city.data
        session["street_name"] = form_search_venue.street_one.data
        session["longitude"] = form_search_venue.longitude.data
        session["latitude"] = form_search_venue.latitude.data
        session["step"] = 2

        #CHECK FOR PRESENCE OF CAFE
        # HANDLE IF RESTAURANT ALREADY EXISTS
        # IF RESTAURANT DOESN'T EXIST SAFE NEW RESTAURANT TO DATA BASE
        cafe_instance = db.session.execute(db.select(Cafe).where(Cafe.name == session["location_name"])).scalar()
        if cafe_instance:
            flash("This This place is already listed! Check it out", "error")
        else:
            session["step"] = 2

            return redirect(url_for("add_place"))
    elif request.method == "POST" and step == 2:

        session["location_name"] = form_venue_info.name.data
        session["street_name"] = form_venue_info.street.data



        # store details in sessions.


        new_cafe = Cafe(
            name= session.get("location_name"),
            img_url= session.get("picture_url"),
            city= session.get("city"),
            address= session.get("street_name"),
            latitude= session.get("latitude"),
            longitude= session.get("longitude"),
            country= session.get("country")
        )

        db.session.add(new_cafe)
        db.session.commit()


        str_city = slugify(session.get("city"))
        str_location_name = slugify(session.get("location_name"))

        #then clear session
        return redirect(url_for("review_venue_info", city=str_city, cafe_name=str_location_name))


    if step == 1:
        return render_template("add.html", form=form_search_venue, api_key=GOOGLE_PLACES_API_KEY)
    elif session["step"] == 2:
        # print(step)
        location_name = session.get("location_name", "")
        street_name = session.get("street_name", "")
        return render_template("add_venue.html", form=form_venue_info, name_of_venue=location_name, street=street_name, step=step)





@app.route("/<location>")
def show_venue(location):
    print(f"location is {location}")
    #reads db for cafes with specified location.
    cafe = db.session.execute(db.select(Cafe).where(Cafe.city == location)).scalars()
    cafes_list = cafe.all()
    print(cafes_list)
    # print(len(cafes_list))

    return render_template("show-venue.html", cafes_list=cafes_list, location=location)



@app.route("/<path:city>/<path:cafe_name>/review", methods=["POST", "GET"])
def review_venue_info(city, cafe_name):
    normal_cafe_name = de_slugify(cafe_name)

    if request.method == "POST":
        # Validates CSRF FORGERY
        session_csrf_token = session.get("csrf_token")
        form_csrf = request.form.get("csrf_token")

        if session_csrf_token != form_csrf:
            return 'CSRF token is missing or invalid', 400

        # EXTRACTS FORM DATA, AND SAVE TO VARIABLE
        wifi = request.form.get("wifi-options")
        power_sockets = request.form.get("power-sockets")
        length_of_work = request.form.get("duration-for-work")
        tables_and_chairs = request.form.get("chairs-comfortable")
        is_it_quiet = request.form.get("it-quiet")
        audio_and_video = request.form.get("audio-video-calls")

        other_people_working = request.form.get("people-working")
        group_tables = request.form.get("group-tables")

        coffee_available = request.form.get("coffee-available")
        food_offered = request.form.get("food-offered")
        veggie_options = request.form.get("veggie-options")
        alcohol_offered = request.form.get("alcohol-offered")
        credit_cards = request.form.get("credit-cards")

        natural_light = request.form.get("natural-light")
        outdoor_area = request.form.get("outdoor-area")
        how_large = request.form.get("large-space")
        restroom = request.form.get("restroom")
        wheelchair_accessible = request.form.get("wheelchair-access")
        air_conditioned = request.form.get("air-conditioned")
        smoke_free = request.form.get("smoke-free")
        pet_friendly = request.form.get("pet-friendly")
        parking_space = request.form.get("parking-space")

        summary = request.form.get("summary")

        # GET ID OF CAFE AND USE TO STORE IN DB
        cafe_instance = db.session.execute(db.select(Cafe).where(Cafe.name == normal_cafe_name)).scalar()
        cafe_id = cafe_instance.id

        # STORE VARIABLES IN DATABASE INSTANCE
        new_review = Review(
            wifi=wifi,
            power_sockets=power_sockets,
            length_of_work=length_of_work,
            tables_and_chairs=tables_and_chairs,
            is_it_quiet=is_it_quiet,
            audio_and_video=audio_and_video,
            other_people_working=other_people_working,
            group_tables=group_tables,
            coffee_available=coffee_available,
            food_offered=food_offered,
            veggie_options=veggie_options,
            alcohol_offered=alcohol_offered,
            credit_cards=credit_cards,
            natural_light=natural_light,
            outdoor_area=outdoor_area,
            how_large=how_large,
            restroom=restroom,
            wheelchair_accessible=wheelchair_accessible,
            air_conditioned=air_conditioned,
            smoke_free=smoke_free,
            pet_friendly=pet_friendly,
            parking_space=parking_space,
            summary=summary,
            restaurant_id=cafe_id
        )

        # ADDS TO DATABASE
        db.session.add(new_review)
        db.session.commit()

        #CLEAR SESSION IN NEXT ROUTE
        session.clear()
        return redirect(url_for("home"))



    location_name = session.get("location_name", "")
    csrf_token = secrets.token_hex(16)
    session["csrf_token"] = csrf_token

    return render_template("review.html", location=location_name, csrf_token=csrf_token, city=city, cafe=cafe_name)




if __name__ == "__main__":
    app.run(debug=True)


"""SHOW VENUE"""
"""WRITE LOGIC TO COVERT REVIEW INPUT TO CUSTOM STYLES.





































"""
