import itsdangerous
from itsdangerous.serializer import Serializer
from itsdangerous import URLSafeTimedSerializer
import smtplib
import redis

from datetime import datetime

import flask_login
import werkzeug.security
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, Blueprint
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, Float, ForeignKey, DateTime
# from sqlalchemy.sql.functions import current_user

from forms import SearchVenue
from forms import VenueInfo
from forms import RegisterForm
from forms import LoginForm, DashboardForm
from reviewquestions import survey_data

import secrets
import os
import re
from typing import List
from functools import wraps

import requests
from werkzeug.security import generate_password_hash, check_password_hash

# from flask_bootstrap import Bootstrap5









app = Flask(__name__)
# key = secrets.token_hex(16)
# app.secret_key = key
app.secret_key = os.environ.get("APP_SECRET_KEY")

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



#LOGIN MANAGER
login_manager = LoginManager()
login_manager.init_app(app)


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
    status: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    user_review: Mapped["Review"] = relationship(back_populates="input_restaurant")

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    surname: Mapped[str] = mapped_column(String(500), nullable=False)
    city: Mapped[str] = mapped_column(String(500), nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    verified: Mapped[bool] = mapped_column(nullable=False, default=False)
    opened: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow())



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

#Defines user blueprint


with app.app_context():
    db.create_all()



GOOGLE_PLACES_API_KEY = os.environ.get("API")


"""CREATE DECORATOR THAT RESTRICS VIEW CAPABILITYES UNTIL EMAIL HAS BEEN VERIFIED"""





def slugify(text):
    stringed_text = str(text)
    text = stringed_text.replace(" ", "-")

    return text

def de_slugify(slugified_text):
    normalised_text = str(slugified_text).replace("-", " ")

    return normalised_text


#LOGIN MANAGER
@login_manager.user_loader
def load_user(user_id):
    user = db.get_or_404(User, int(user_id))

    return user



#SENDER
master_mail = os.environ.get("MASTER_EMAIL")
password = os.environ.get("MASTER_EMAIL_PASSWORD")

def send_mail(verification_url, user_email):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(master_mail, password)
        connection.sendmail(master_mail, user_email, msg=f"Subject:Verify Your Email\n\nPlease verify your email here {verification_url}")

    return jsonify({"status": "sent"})


#SERIALIZER FOR EMAIL VERIFICATION
secret_key = os.environ.get("SERIALIZER_KEY")
serializer = URLSafeTimedSerializer(secret_key, "email-verify")

def make_token(email: str) -> str:
    token = serializer.dumps(email, salt="email-verify")

    return token


def de_serializer(token: str, expiration=3600):
    try:
        email = serializer.loads(token, max_age=3600, salt="email-verify")
        return email
    except itsdangerous.SignatureExpired:
        return None
    except itsdangerous.BadSignature:
        return None


#EMAIL-VERIFICATION DECORATOR FUNCTION
def email_verification_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        is_verified = current_user.verified

        if not is_verified:
            return redirect(url_for("protected.unverified"))

        return f(*args, **kwargs)
    return wrapper


#INITIALIZE REDIS CLASS

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)
#MEMURAI
print(redis_client.ping())




# RETURNS LIST OF PLACE TO THE FRONT END, SO USER CAN EASILY GET FEEDBACK IF THEY ENTER CAFE THAT ALREADY EXIST
# @app.route("/api/restaurants")
# def get_list_of_places():
#     list_of_places = []
#     with app.app_context():
#         restaurants = db.session.execute(db.select(Cafe).order_by(Cafe.id)).scalars().all()
#
#     for restaurant in restaurants:
#         print(restaurant.name)
#         list_of_places.append(restaurant.name)
#
#     return list_of_places
#
#
# #view searches through db and gets result for latitude and longitude in list
# @app.route("/api/latlong")
# def get_lat_and_long():
#     lat_long_list = []
#     city = request.args.get("city")
#
#     result = db.session.execute(db.select(Cafe).where(Cafe.city == city)).scalars().all()
#
#     for restaurant in result:
#         latitude = restaurant.latitude
#         longitude = restaurant.longitude
#
#         lat_long_list.append({"lat": latitude, "lng": longitude, "title": restaurant.name})
#
#
#     return lat_long_list  #returns list of latitude and longitude of each location


#DEFINE BLUEPRINTS
unprotected = Blueprint("unprotected", __name__)
protected = Blueprint("protected", __name__)




#ROUTES
@unprotected.route("/")
@cache.cached(timeout=50)
def home():

    print("Current user:", current_user)
    #Reads DB and stores location in list, conditional statement ensures there is no repetition of location
    cafe = db.session.execute(db.select(Cafe).order_by(Cafe.id)).scalars()


    cafes = cafe.all()

    location_list = []
    for items in cafes:
        location = items.city
        #TO AVOID REPETITION OF LOCATION
        if location not in location_list:
            location_list.append(location)

    #ENSURES ALL SESSION DATA IS CLEARED INCASE USER COMES TO HOME ROUTE FRPM ADD_PLACE WHERE SESSION IS USED HEAVILY TO STORE TEMP DATA
    # if session:
    #     session.clear()
    reverse_geo_location = session.get("reverse_geocoding_location")
    # print(f"hello {reverse_geo_location}")
    # print(f"{session['reverse_geocoding_location']} Bye Bye")
    if reverse_geo_location:
        return render_template("index.html", location_list=location_list, api=GOOGLE_PLACES_API_KEY, home_location=reverse_geo_location)
    else:
        # if session:
        #     session.clear()

        return render_template("index.html", location_list=location_list, api=GOOGLE_PLACES_API_KEY)

@login_required
@protected.route("/add", methods=["GET", "POST"])
def add_place():
    # print(current_user.is_authenticated)


    form_search_venue = SearchVenue()
    form_venue_info = VenueInfo()

    # if "step" not in session:
    #     session["step"] = 1
    # SET STEP = 1 IF STEP IS NOT IN SESSION
    step = session.get("step", 1)

    #THIS BIT OF CODE HAPPENS WHEN USER SUBMITS THE FIRST FORM
    #NO CSRF VALIDATION
    if request.method == "POST" and step == 1:
    # if form_search_venue.validate_on_submit() and step == 1:
        #store details in sessions.
        session["location_name"] = form_search_venue.location.data
        session["picture_url"] = form_search_venue.photo.data
        session["country"] = form_search_venue.country.data
        session["city"] = form_search_venue.city.data
        session["street_name"] = form_search_venue.street_one.data
        session["longitude"] = form_search_venue.longitude.data
        session["latitude"] = form_search_venue.latitude.data
        session["step"] = 2

        return redirect(url_for("protected.add_place"))
    # NO CSRF VALIDATION
    elif request.method == "POST" and step == 2:
    # elif form_venue_info.validate_on_submit() and step == 2:
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
            country= session.get("country"),
            status= True
        )

        db.session.add(new_cafe)
        db.session.commit()

        cafe_instance = Cafe.query.filter_by(
            name=session.get("location_name")
        ).first()

        # READ AND CREATE SEMI COMPLETE REVIEW RECORD TO AVOID ERROR IN show_location.
        new_review = Review(
            wifi="",
            power_sockets="",
            length_of_work="",
            tables_and_chairs="",
            is_it_quiet="",
            audio_and_video="",
            other_people_working="",
            group_tables="",
            coffee_available="",
            food_offered="",
            veggie_options="",
            alcohol_offered="",
            credit_cards="",
            natural_light="",
            outdoor_area="",
            how_large="",
            restroom="",
            wheelchair_accessible="",
            air_conditioned="",
            smoke_free="",
            pet_friendly="",
            parking_space="",
            summary="",
            restaurant_id=cafe_instance.id,
        )
        db.session.add(new_review)
        db.session.commit()

        #slugify both city and location name as they both will be used for url building in the next view
        str_city = slugify(session.get("city"))
        str_location_name = slugify(session.get("location_name"))
        # print(str_location_name)

        #redirect to review_venue_info view.
        return redirect(url_for("protected.review_venue_info", city=str_city, cafe_name=str_location_name))


    if step == 1:
        return render_template("add.html", form=form_search_venue, api_key=GOOGLE_PLACES_API_KEY)
    elif session["step"] == 2:
        # print(step)
        location_name = session.get("location_name", "")
        street_name = session.get("street_name", "")
        return render_template("add_venue.html", form=form_venue_info, name_of_venue=location_name, street=street_name, step=step)





@unprotected.route("/<location>")
def show_venue(location):
    # print(f"location is {location}")
    #reads db for cafes with specified location.
    cafe = db.session.execute(db.select(Cafe).where(Cafe.city == location)).scalars()
    cafes_list = cafe.all()

    return render_template("show-venue.html", cafes_list=cafes_list, location=location, api_key=GOOGLE_PLACES_API_KEY)

#LOGIN REQUIRED TO POST
#uses slugified city and cafe_name
@login_required
@protected.route("/<path:city>/<path:cafe_name>/review", methods=["POST", "GET", "PUT", "PATCH"])
def review_venue_info(city, cafe_name):

    de_sluged_cafe_name = de_slugify(cafe_name)
    normal_cafe_name = session.get("location_name")
    location_name = session.get("location_name", "")
    # print(f"{normal_cafe_name} session")
    # print(f"{cafe_name} cafe_name")
    # print(f"{de_sluged_cafe_name} deslugged")

    cafe_db = db.session.execute(db.select(Cafe).where(Cafe.name == de_sluged_cafe_name)).scalar()
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
        # print(cafe_instance)
        if not cafe_instance:
            print("Gobe")

        cafe_id = cafe_db.id
        # new_review_instance = db.get_or_404(Review, cafe_id)

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

        # # ADDS TO DATABASE
        db.session.add(new_review)
        db.session.commit()

        #CLEAR SESSION IN NEXT ROUTE
        session.clear()

        return redirect(url_for("show_location", city=city, name=de_sluged_cafe_name))
    elif request.method == "POST" and review_db:
        #dynamically only update what has been filled, if user does not fill other parts, do not update them.
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
        # cafe_instance = db.session.execute(db.select(Cafe).where(Cafe.name == de_sluged_cafe_name)).scalar()
        # cafe_id = cafe_instance.id
        cafe_instance = Cafe.query.filter_by(
            name=de_sluged_cafe_name
        ).first()
        cafe_id = cafe_instance.id


        review_instance =  Review.query.get(cafe_id)

        #GET REVIEW DB INSTANCE TO REPLACE



        # review_instance = db.session.execute(db.select(Review).where(Review.id == cafe_id)).scalar()

        review_instance.wifi = wifi
        review_instance.power_sockets = power_sockets
        review_instance.length_of_work = length_of_work
        review_instance.tables_and_chairs = tables_and_chairs
        review_instance.is_it_quiet = is_it_quiet
        review_instance.audio_and_video = audio_and_video
        review_instance.other_people_working = other_people_working
        review_instance.group_tables = group_tables
        review_instance.coffee_available = coffee_available
        review_instance.food_offered = food_offered
        review_instance.veggie_options = veggie_options
        review_instance.alcohol_offered = alcohol_offered
        review_instance.credit_cards = credit_cards
        review_instance.natural_light = natural_light
        review_instance.outdoor_area = outdoor_area
        review_instance.how_large = how_large
        review_instance.restroom = restroom
        review_instance.wheelchair_accessible = wheelchair_accessible
        review_instance.air_conditioned = air_conditioned
        review_instance.smoke_free = smoke_free
        review_instance.pet_friendly = pet_friendly
        review_instance.parking_space = parking_space
        review_instance.summary = summary

        db.session.commit()

        # print("im happening")

        return redirect(url_for("show_location", city=city, name=de_sluged_cafe_name))

    #if review is being edited, hence existed previously, run first condition, else  run second condition
    if review_db:
        summary_rating = review_db.summary
        data_dict = {

            "PRODUCTIVITY": [review_db.wifi, review_db.power_sockets, review_db.length_of_work, review_db.tables_and_chairs, review_db.is_it_quiet, review_db.audio_and_video],

            "COMMUNITY": [review_db.other_people_working, review_db.group_tables],

            "SERVICE": [review_db.coffee_available, review_db.food_offered, review_db.veggie_options, review_db.alcohol_offered, review_db.credit_cards],

            "SPACE": [review_db.natural_light, review_db.outdoor_area, review_db.how_large, review_db.restroom, review_db.wheelchair_accessible, review_db.air_conditioned, review_db.smoke_free, review_db.pet_friendly, review_db.parking_space]
        }
        csrf_token = secrets.token_hex(16)
        session["csrf_token"] = csrf_token
        return render_template("review.html", location=location_name, csrf_token=csrf_token, city=city, cafe=de_sluged_cafe_name, summary=summary_rating, survey_data=survey_data, review_data=data_dict)
    else:
        csrf_token = secrets.token_hex(16)
        session["csrf_token"] = csrf_token
        data_dict = {}
        return render_template("review.html", location=location_name, csrf_token=csrf_token, city=city, cafe=de_sluged_cafe_name, survey_data=survey_data, review_data=data_dict)



@unprotected.route("/cities")
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


    # print(city_dict)

    # ENSURES ALL SESSION DATA IS CLEARED INCASE USER COMES TO HOME ROUTE FROM ADD_PLACE WHERE SESSION IS USED HEAVILY TO STORE TEMP DATA
    # if session:
    #     session.clear()


    return render_template("cities.html", city_dict=city_dict)

@protected.route("/<city>/<name>")
@login_required
@email_verification_required
def show_location(city, name):
    #open db and fetch all values
    cafe_info = db.session.execute(db.select(Cafe).where(Cafe.name == name)).scalar()
    cafe_id = cafe_info.id
    location_address = cafe_info.address

    #open review section of db
    review_info = db.session.execute(db.select(Review).where(Review.id == cafe_id)).scalar()
    # review_info = Review.query.filter_by(
    #     id=cafe_id
    # ).first()

    if not review_info:
        # print("Ela")
        return redirect(url_for("review_venue_info", city=city, cafe_name=name))

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


@protected.route("/users", methods=["GET"])
@login_required
@email_verification_required
def dashboard():
    dashboard_form = DashboardForm()
    # print(f"my name is {current_user.id} id")
    user = current_user
    # photo = user.photo  to be done later
    user_data = {
       "first_name": user.name,
        "surname": user.surname,
        "email": user.email,
    }
    #PUT FORMVALIDATE TO ACCOMODATE UPDATE TO USER PROFILE DETAILS



    return render_template("dashboard.html", user_data=user_data, form=dashboard_form)



@unprotected.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data

        user = db.session.execute(db.select(User).where(User.email == email)).scalar_one_or_none()

        if not user:
            flash("User Does not Exist", "error")
            return  redirect(url_for("unprotected.register"))
        else:
            is_password = werkzeug.security.check_password_hash(user.password, password)

            if not is_password:
                flash("Invalid Details", "error")
                return redirect(url_for("unprotected.login"))
            else:

                flash("Login Success", "info")
                login_user(user)

                return redirect(url_for("protected.dashboard"))

    return render_template("login.html", form=login_form)

def recover_account():
    pass


@unprotected.route("/logout")
def logout():
    logout_user()

    return redirect(url_for("unprotected.login"))


@unprotected.route("/verify-email/<token>")
def verify_email(token):
    #CHECK IF CURRENT USER IS SAME WITH EMAIL FROM DESERIALIZED TOKEN.
    email = de_serializer(token)
    # print(email)

    #IF TOKEN HAS BEEN TAMPERED WITH OR EXPIRED
    if not email:
        flash("Link Expired", "danger")
        # return redirect(url_for(""))    #resend verification link page
        pass

    #CHECK USER IN DB
    user = db.session.execute(db.select(User).where(User.email == email)).scalar_one_or_none()
    #IF WRONG EMAIL WHICH WOULD MOSTLIKELY NOT HAPPEN EXCEPT USER TAMPERS WITH TOKEN
    if not user:
        flash("This Email is Not Registered to Any Account", "danger")

        return redirect(url_for("unprotected.register"))

    #IF USER HAD ALREADY VERIFIED EMAIL.
    if user.verified:
        flash("Email Previously Verified", "success")
        return redirect(url_for("protected.login"))

    user.verified = True
    db.session.commit()
    login_user(user)
    """redirect to unverified, but show diff ui"""
    return redirect(url_for("protected.dashboard"))







# @app.route("/register", methods=["GET", "POST"])
@unprotected.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegisterForm()
    # csrf_token = secrets.token_hex(16)
    # session["csrf_token"] = csrf_token

    if register_form.validate_on_submit(): #AUTOMATICALLY VALIDATES CSRF
        email = register_form.email.data
        name = register_form.name.data
        surname = register_form.surname.data
        city = register_form.city.data
        un_hashed_password = register_form.password.data
        un_hashed_password_confirmation = register_form.password_confirm.data

        #CHECK IF USER ALREADY EXIST
        user_exist = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if not user_exist:
            #HARSD PASSWORD
            # print("Hello")
            hashed_password = werkzeug.security.generate_password_hash(un_hashed_password, method="scrypt", salt_length=16)

            user = User(
                email=email,
                name=name,
                surname=surname,
                city=city,
                password=hashed_password
            )

            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("success", "info")

            #SEND VERIFICATION EMAIL
            # send_verification_email(email)
            token = make_token(email)
            verify_url = url_for("unprotected.verify_email", token=token, _external=True)
            # print(verify_url)
            send_mail(verify_url, email)

            return redirect(url_for("protected.unverified")) #CHANGE TO DASHBOARD or unverified
        else:
            flash("User Already Exist", "error")
            return redirect(url_for("unprotected.register"))





    return render_template("register.html", form=register_form)

@protected.route("/unverified-mail")
@login_required
def unverified():

    return render_template("unverified-page.html")




# login_manager.login_view = "unprotected.register"

"""                                            FUNCTIONS                                                    """
def can_send_email(user_id):
    key = f"resend_verification:{user_id}"
    can_send = redis_client.exists(key)  #if key exist then user cannot send, if key does not exist, them user can send

    #if key does not exist, then set new key with timer/expiry equals 30 secs then return truw
    if not can_send:
        redis_client.set(key, 1, nx=True, ex=30)
        return True

    return False





"""                                            AJAX                                                          """

@app.route("/resend-verification", methods=["POST"])
def resend_verification_email():
    send_the_mail = can_send_email(current_user.id)

    if send_the_mail:
        #check database for the last time user resent verification mail, comapre with current time if difference less tnan 30 sec return abort else ok
        email = current_user.email
        token = make_token(email)
        verify_url = url_for("unprotected.verify_email", token=token, _external=True)
        response = send_mail(verify_url, email)
        # print(response.data)

        if response.data:
            return jsonify({"message": "sent"})
    else:
        return jsonify({"message": "Please wait before sending"}), 429 #too many request


#HANDLES A PATCH REQUEST THAT EDITS THE CLOSED STATUS IN THE DB
@app.route("/restaurant/closed-or-opened", methods=["PATCH"])
def report_closed_or_opened():
    request_body = request.get_json()
    restaurant_name = request_body.get("name")
    restaurant_to_update = db.session.execute(db.select(Cafe).where(Cafe.name == restaurant_name)).scalar()
    status = restaurant_to_update.status

    if status:
        restaurant_to_update.status = False
        db.session.commit()

        return jsonify({"status": "closed"})
    else:
        restaurant_to_update.status = True
        db.session.commit()

        return jsonify({"status": "opened"})




#USES RESTAURANT NAME FROM FRONTEND TO CHECK THE OPEN STATUS FROM THE DB
@app.route("/restaurant/status", methods=["GET"])
def check_restaurant_status():
    restaurant_name = request.args.get("name")
    db_restaurant = db.session.execute(db.select(Cafe).where(Cafe.name == restaurant_name)).scalar()

    if db_restaurant:
        status = db_restaurant.status
        if status:
            return jsonify({"status": True})
        else:
            return jsonify({"status": False})

    # ELSE RETURN ERROR OR HANDLE ERROR

#UPDATES SUMMARY VALUE IN DB, RETURNS STATUS WHEN DONE
@app.route("/update/summary", methods=["PATCH"])
def update_summary():
    request_body = request.get_json()
    name_of_restaurant = request_body.get("name")
    summary_value = request_body.get("summary_value")


    #GET DB TO UPDATE
    restaurant_to_update = db.session.execute(db.select(Cafe).where(Cafe.name == name_of_restaurant)).scalar()
    restaurant_id = restaurant_to_update.id

    #GET REVIEW DATABASE
    review_db = db.session.execute(db.select(Review).where(Review.id == restaurant_id)).scalar()

    #UPDATE DB

    review_db.summary = summary_value
    db.session.commit()

    return jsonify({"status": "updated"})


#USES GOOGLE API TO SEARCH FOR USERS CITY USING LONGITUDE AND LATITUDE
@app.route("/reverse/geo")
def reverse_geocoding():
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")

    response = requests.get("https://maps.googleapis.com/maps/api/geocode/json",
                            params={
                                "latlng": f"{latitude}, {longitude}",
                                "key": GOOGLE_PLACES_API_KEY
                            })

    response.raise_for_status()
    data = response.json()
    # print(data)
    # print(data.results[0].address_components[3].long_name)
    city = data["results"][0]["address_components"][3]["long_name"]
    # print(city)
    session["reverse_geocoding_location"] = city
    # print(f"{session['reverse_geocoding_location']} inside fetch")


    return jsonify({"city": city})


# RETURNS LIST OF PLACE TO THE FRONT END, SO USER CAN EASILY GET FEEDBACK IF THEY ENTER CAFE THAT ALREADY EXIST
@app.route("/api/restaurants")
def get_list_of_places():
    list_of_places = []
    with app.app_context():
        restaurants = db.session.execute(db.select(Cafe).order_by(Cafe.id)).scalars().all()

    for restaurant in restaurants:
        # print(restaurant.name)
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


#REGISTER BLUEPRINT
app.register_blueprint(unprotected)
app.register_blueprint(protected)

#SET LOGIN VIEW
login_manager.login_view = "unprotected.login"

if __name__ == "__main__":
    app.run(debug=True)





#NEEDS USER LOGIN/REGISTER TO EDIT ANYTHING/ MAKE ADDITION
#NON USER CAN ONLY VIEW STUFF














