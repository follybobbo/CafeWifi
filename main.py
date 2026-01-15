from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
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
        print(restaurant.name)
        list_of_places.append(restaurant.name)

    return list_of_places


#view searches through db and gets result for latitude and longitude in list
@app.route("/api/latlong")
def get_lat_and_long():
    lat_long_list = []
    city = request.args.get("city")

    result = db.session.execute(db.select(Cafe).where(Cafe.city == city)).scalars().all()

    for restaurant in result:
        latitude = restaurant.latitude
        longitude = restaurant.longitude

        lat_long_list.append({"lat": latitude, "lng": longitude, "title": restaurant.name})


    return lat_long_list  #returns list of latitude and longitude of each location







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
            session.clear()
        else:
            session["step"] = 2

            return redirect(url_for("add_place"))
    elif request.method == "POST" and step == 2:

        session["location_name"] = form_venue_info.name.data
        session["street_name"] = form_venue_info.street.data



        # store details in sessions.

        #write new cafe to database
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

        #slugify both city and location name as they both will be used for url building in the next view
        str_city = slugify(session.get("city"))
        str_location_name = slugify(session.get("location_name"))
        print(str_location_name)

        #redirect to review_venue_info view.
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
    # print(f"location is {location}")
    #reads db for cafes with specified location.
    cafe = db.session.execute(db.select(Cafe).where(Cafe.city == location)).scalars()
    cafes_list = cafe.all()
    # print(cafes_list)
    # print(len(cafes_list))

    return render_template("show-venue.html", cafes_list=cafes_list, location=location, api_key=GOOGLE_PLACES_API_KEY)

#LOGIN REQUIRED TO POST
#uses slugified city and cafe_name
@app.route("/<path:city>/<path:cafe_name>/review", methods=["POST", "GET"])
def review_venue_info(city, cafe_name):
    normal_cafe_name = session.get("location_name")
    location_name = session.get("location_name", "")

    cafe_db = db.session.execute(db.select(Cafe).where(Cafe.name == cafe_name)).scalar()
    cafe_id = cafe_db.id
    review_db = db.session.execute(db.select(Review).where(Review.id == cafe_id)).scalar()

    #if user submits review form on first creation of review run first condition, else if review already exists and user
    # wants to update contents of review, run second condition
    if request.method == "POST" and not review_db:
        # Validates CSRF FORGERY
        session_csrf_token = session.get("csrf_token")
        form_csrf = request.form.get("csrf_token")

        if session_csrf_token != form_csrf:
            return 'CSRF token is missing or invalid', 400

        # EXTRACTS FORM DATA, AND SAVE TO VARIABLE
        wifi = request.form.get("wifi")
        power_sockets = request.form.get("sockets")
        length_of_work = request.form.get("duration")
        tables_and_chairs = request.form.get("tables")
        is_it_quiet = request.form.get("quiet")
        audio_and_video = request.form.get("audio")

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
        print(cafe_instance)
        if not cafe_instance:
            print("Gobe")
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

        return redirect(url_for("show_location", city=city, name=normal_cafe_name))
    elif request.method == "POST" and review_db:
        #dynamically only update what has been filled, if user does not fill other parts, do not update them.

        return redirect(url_for("show_location", city=city, name=normal_cafe_name))

    #if review is being edited, hence existed previously, run first condition, else  run second condition
    if review_db:
        summary_rating = review_db.summary
        csrf_token = secrets.token_hex(16)
        session["csrf_token"] = csrf_token
        return render_template("review.html", location=location_name, csrf_token=csrf_token, city=city, cafe=cafe_name, summary=summary_rating, survey_data=survey_data)
    else:
        csrf_token = secrets.token_hex(16)
        session["csrf_token"] = csrf_token
        return render_template("review.html", location=location_name, csrf_token=csrf_token, city=city, cafe=cafe_name, survey_data=survey_data)

@app.route("/cities")
def show_cities():
    city_dict = {}
    data = db.session.execute(db.select(Cafe).order_by(Cafe.country)).scalars()

   #use google api to get current country, and make current country first on the list of countries/
    for rows in data:
        country = rows.country

        country_list = city_dict.keys()

        if country in country_list:
            city_list = city_dict.get(country)

            if rows.city not in city_list:
                city_list.append(rows.city)
        else:
            city_dict[country] = [rows.city]


    print(city_dict)





    return render_template("cities.html", city_dict=city_dict)


@app.route("/<city>/<name>")
def show_location(city, name):
    #open dv and fetch all values
    cafe_info = db.session.execute(db.select(Cafe).where(Cafe.name == name)).scalar()
    cafe_id = cafe_info.id
    location_address = cafe_info.address

    #open review section of db

    review_info = db.session.execute(db.select(Review).where(Review.id == cafe_id)).scalar()
    summary = review_info.summary


    data_dict = {

        "PRODUCTIVITY": {
            #display_text: [tooltip_text, data_for_review]
            "stable wifi": ["is there wifi", review_info.wifi],
            "power sockets": ["Is it easy to find power sockets", review_info.power_sockets],
            "length of work": ["How long can you comfortably stay and work ?", review_info.length_of_work],
            "tables and chairs": ["Are tables and chairs comfortable for work ?", review_info.tables_and_chairs],
            "is it quiet": ["Is it quiet ?", review_info.is_it_quiet],
            "audio and video": ["Can you comfortably make audio/video calls ?", review_info.audio_and_video]
        },
        "COMMUNITY": {
            "people working": ["Is it common to see other people working ?", review_info.other_people_working],
            "group tables": ['Are there group tables (for 6+ people)', review_info.group_tables]
        },
        "SERVICE": {
            "coffee": ["Is coffee available", review_info.coffee_available],
            "food": ["Is food offered", review_info.food_offered],
            "veggie": ["Are there veggie options", review_info.veggie_options],
            "Alcohol": ["Is alcohol offered", review_info.alcohol_offered],
            "credit cards": ["Are credit cards accepted ?", review_info.credit_cards]
        },
        "SPACE": {
            "Natural light": ["Is the space full of natural light", review_info.natural_light],
            "Outdoor area": ["Is there an outdoor area?", review_info.outdoor_area],
            "Spacious": ["How large is the place ?", review_info.how_large],
            "Restroom": ["Is there a restroom", review_info.restroom],
            "Accessible": ["Is it easily accessible with a wheelchair", review_info.wheelchair_accessible],
            "Air conditioned": ["Is the place air conditioned ?", review_info.air_conditioned],
            "Smoke free": ["Is the space smoke free", review_info.smoke_free],
            "Pet friendly": ["Is it pet friendly", review_info.pet_friendly],
            "Parking": ["Is there a parking space", review_info.parking_space]
        }
    }

    return render_template("location.html", name=name, city=city, img_url=cafe_info.img_url, data_dict=data_dict, location_address=location_address, summary=summary)



if __name__ == "__main__":
    app.run(debug=True)





#NEEDS USER LOGIN/REGISTER TO EDIT ANYTHING/ MAKE ADDITION
#NON USER CAN ONLY VIEW STUFF














