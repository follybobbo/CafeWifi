from app.extensions import login_manager
from app.services import (get_user, redis_client, write_new_cafe, query_db_and_filter_by, write_record_to_review_db,
                          get_single_cafe_by_cafe_name, get_review_record_using_id, update_review_record,
                          get_data_dict_for_show_location, create_user_data_for_dashboard)
from flask import session, Blueprint, request, redirect, url_for, render_template, flash, jsonify
from app.forms import SearchVenue, VenueInfo, DashboardForm
from app import limiter
from flask_login import login_required, current_user
from app.Utils import slugify, de_slugify, survey_data
from dotenv import load_dotenv
import os
import secrets
from app.decorators import email_verification_required

load_dotenv()



protected = Blueprint("protected", __name__)
GOOGLE_PLACES_API_KEY = os.environ.get("API")



@login_manager.user_loader
def load_user(user_id):
    user = get_user(int(user_id))

    return user



@protected.route("/add", methods=["GET", "POST"])
@limiter.limit("10/minute")
@limiter.limit("2/second")
@login_required
def add_place():
    form_search_venue = SearchVenue()
    form_venue_info = VenueInfo()

    # if "step" not in session:
    #     session["step"] = 1
    # SET STEP = 1 IF STEP IS NOT IN SESSION
    step = session.get("step", 1)

    #THIS BIT OF CODE HAPPENS WHEN USER SUBMITS THE FIRST FORM
    #NO CSRF VALIDATION

    if request.method == "POST" and step == 1:
        #create csrf services----------------------------------------------- creation and validation of csrf tokens
        session_csrf = session.get("csrf_token")
        form_csrf = request.form.get("csrf_token")
        if session_csrf != form_csrf:
            return jsonify({"Invalid Csrf Token"}), 400   #bad request

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
    # store details in sessions.
        session_csrf = session.get("csrf_token")
        form_csrf = request.form.get("csrf_token")
        if session_csrf != form_csrf:
            return jsonify({"Invalid Csrf Token"}), 400  # bad request

        session["location_name"] = form_venue_info.name.data
        session["street_name"] = form_venue_info.street.data

        #write new cafe to database
        write_new_cafe(session.get("location_name"), session.get("picture_url"), session.get("city"),
                                     session.get("street_name"), session.get("latitude"), session.get("longitude"),
                                     session.get("country"), True)

        cafe_instance = query_db_and_filter_by(filter_value=session.get("location_name"))

        # READ AND CREATE SEMI COMPLETE REVIEW RECORD TO AVOID ERROR IN show_location.
        write_record_to_review_db("", "", "", "", "",
                                                  "", "", "", "",
                                                  "", "", "", "",
                                                  "", "", "", "",
                                                  "", "", "", "",
                                                  "", "", cafe_instance.id)


        #slugify both city and location name as they both will be used for url building in the next view
        str_city = slugify(session.get("city"))
        str_location_name = slugify(session.get("location_name"))

        #redirect to review_venue_info view.
        return redirect(url_for("protected.review_venue_info", city=str_city, cafe_name=str_location_name))


    if step == 1:
        csrf_token = secrets.token_hex(16)
        session["csrf_token"] = csrf_token

        return render_template("add.html", form=form_search_venue, api_key=GOOGLE_PLACES_API_KEY, csrf_token=csrf_token)
    elif session["step"] == 2:
        csrf_token = secrets.token_hex(16)
        session["csrf_token"] = csrf_token

        location_name = session.get("location_name", "")
        street_name = session.get("street_name", "")
        return render_template("add_venue.html", form=form_venue_info, name_of_venue=location_name, street=street_name, step=step, csrf_token=csrf_token)



@protected.route("/<path:city>/<path:cafe_name>/review", methods=["POST", "GET", "PUT", "PATCH"])
@login_required
def review_venue_info(city, cafe_name):

    de_sluged_cafe_name = de_slugify(cafe_name)
    normal_cafe_name = session.get("location_name")
    location_name = session.get("location_name", "")

    cafe_db = get_single_cafe_by_cafe_name(de_sluged_cafe_name)
    cafe_id = cafe_db.id

    # at  this point will always exists cause it will always be written in add place route.
    review_db = get_review_record_using_id(cafe_id)

    if request.method == "POST" and review_db:
        # dynamically only update what has been filled, if user does not fill other parts, do not update them.
        session_csrf_token = session.get("csrf_token")
        form_csrf = request.form.get("csrf_token")

        if session_csrf_token != form_csrf:
            return jsonify({"Error": "CSRF token is missing or invalid"}), 400

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
        cafe_instance = query_db_and_filter_by(filter_value=de_sluged_cafe_name)
        cafe_id = cafe_instance.id
        review_instance = get_review_record_using_id(cafe_id)

        # review_instance =  Review.query.get(cafe_id)

        # GET REVIEW DB INSTANCE TO REPLACE

        # review_instance = db.session.execute(db.select(Review).where(Review.id == cafe_id)).scalar()
        result = update_review_record(review_instance, wifi, power_sockets, length_of_work,
                                                        tables_and_chairs, is_it_quiet, audio_and_video,
                                                        other_people_working,
                                                        group_tables, coffee_available, food_offered, veggie_options,
                                                        alcohol_offered, credit_cards, natural_light, outdoor_area,
                                                        how_large,
                                                        restroom, wheelchair_accessible, air_conditioned, smoke_free,
                                                        pet_friendly,
                                                        parking_space, summary)
        print(result)

        return redirect(url_for("show_location", city=city, name=de_sluged_cafe_name))

        # if review is being edited, hence existed previously, run first condition, else  run second condition
        # if review_db:
    summary_rating = review_db.summary
    prepopulated_data_dict = {

        "PRODUCTIVITY": [review_db.wifi, review_db.power_sockets, review_db.length_of_work,
                                review_db.tables_and_chairs, review_db.is_it_quiet, review_db.audio_and_video],

        "COMMUNITY": [review_db.other_people_working, review_db.group_tables],

        "SERVICE": [review_db.coffee_available, review_db.food_offered, review_db.veggie_options,
                    review_db.alcohol_offered, review_db.credit_cards],

        "SPACE": [review_db.natural_light, review_db.outdoor_area, review_db.how_large, review_db.restroom,
                    review_db.wheelchair_accessible, review_db.air_conditioned, review_db.smoke_free,
                    review_db.pet_friendly, review_db.parking_space]
        }
    csrf_token = secrets.token_hex(16)
    session["csrf_token"] = csrf_token
    return render_template("review.html", location=location_name, csrf_token=csrf_token, city=city,
                            cafe=de_sluged_cafe_name, summary=summary_rating, survey_data=survey_data,
                            review_data=prepopulated_data_dict)
        # else:
        #     csrf_token = secrets.token_hex(16)
        #     session["csrf_token"] = csrf_token
        #     data_dict = {}
        #     return render_template("review.html", location=location_name, csrf_token=csrf_token, city=city,
        #                            cafe=de_sluged_cafe_name, survey_data=survey_data, review_data=data_dict)


@protected.route("/<city>/<name>")
@login_required
@email_verification_required
def show_location(city, name):
    # print(name)
    #open db and fetch all values
    cafe_info = get_single_cafe_by_cafe_name(name)
    cafe_id = cafe_info.id
    location_address = cafe_info.address

    #open review section of db
    review_info = get_review_record_using_id(cafe_id)

    #This should never run.
    if not review_info:
        # print("Ela")
        return redirect(url_for("review_venue_info", city=city, cafe_name=name))

    summary = review_info.summary
    data_dict = get_data_dict_for_show_location(review_instance=review_info)

    return render_template("location.html", name=name, city=city, img_url=cafe_info.img_url,
                           data_dict=data_dict, location_address=location_address, summary=summary)



@protected.route("/users", methods=["GET"])
@login_required
@email_verification_required
def dashboard():
    dashboard_form = DashboardForm()
    user = current_user
    # photo = user.photo  to be done later
    user_data = create_user_data_for_dashboard(user)

    #PUT FORMVALIDATE TO ACCOMODATE UPDATE TO USER PROFILE DETAILS ??? Nigga!

    return render_template("dashboard.html", user_data=user_data, form=dashboard_form)


@protected.route("/unverified-mail")
@login_required
def unverified():

    return render_template("unverified-page.html")
