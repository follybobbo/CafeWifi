from flask import Blueprint, render_template, session, redirect, url_for, flash
from app.services import (get_all_cafes_and_order_by_id, get_cafe_city_list, get_all_cafe_instance_by_location,
                          get_all_cafe_and_order_by_country, create_country_city_list_dictionary, get_user_by_email,
                          de_serializer, update_user_email_verification_status, create_new_user, make_token, send_mail)
from dotenv import load_dotenv
import os
from app import cache, limiter
from app.decorators import login_token_bucket_limiter
from flask_login import login_user, logout_user
from app.forms import LoginForm, RegisterForm
import werkzeug.security


load_dotenv()



unprotected = Blueprint("unprotected", __name__)
GOOGLE_PLACES_API_KEY = os.environ.get("API")




#ROUTES
@unprotected.route("/")
@limiter.limit("10/minute")
@limiter.limit("2/second")
@cache.cached(timeout=50)
def home():

    # print("Current user:", current_user)
    #Reads DB and stores location in list, conditional statement ensures there is no repetition of location
    session.pop("step", None)
    result = get_all_cafes_and_order_by_id()
    cafes = result.all()

    location_list = []
    location_list = get_cafe_city_list(cafes, location_list)

    #ENSURES ALL SESSION DATA IS CLEARED INCASE USER COMES TO HOME ROUTE FRPM ADD_PLACE WHERE SESSION IS USED HEAVILY TO STORE TEMP DATA
    reverse_geo_location = session.get("reverse_geocoding_location")

    if reverse_geo_location:
        return render_template("index.html", location_list=location_list, api=GOOGLE_PLACES_API_KEY, home_location=reverse_geo_location)
    else:
        return render_template("index.html", location_list=location_list, api=GOOGLE_PLACES_API_KEY)



@unprotected.route("/<location>")
@limiter.limit("10/minute")
@limiter.limit("2/second")
def show_venue(location):
    #reads db for cafes with specified location.
    cafe = get_all_cafe_instance_by_location(location)
    cafes_list = cafe.all()

    return render_template("show-venue.html", cafes_list=cafes_list, location=location, api_key=GOOGLE_PLACES_API_KEY)


@unprotected.route("/cities")
@limiter.limit("10/minute")
@limiter.limit("2/second")
def show_cities():
    storage = {}
    #STORAGE FORMAT BELOW
    # storage = {
    #     country: country_list
    # }
    cafe_instance_ordered_by_country = get_all_cafe_and_order_by_country()
    storage = create_country_city_list_dictionary(cafe_instance_ordered_by_country, storage)

    return render_template("cities.html", city_dict=storage)


@unprotected.route("/login", methods=["GET", "POST"])
@login_token_bucket_limiter(limit=10, rate=5)
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data

        user = get_user_by_email(email)

        # user = db.session.execute(db.select(User).where(User.email == email)).scalar_one_or_none()

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

        return redirect(url_for("unprotected.login"))

    #CHECK USER IN DB
    user = get_user_by_email(email)

    #IF WRONG EMAIL WHICH WOULD MOSTLIKELY NOT HAPPEN EXCEPT USER TAMPERS WITH TOKEN
    if not user:
        flash("This Email is Not Registered to Any Account", "danger")

        return redirect(url_for("unprotected.register"))

    #IF USER HAD ALREADY VERIFIED EMAIL.
    if user.verified:
        flash("Email Previously Verified", "success")
        return redirect(url_for("protected.login"))

    update_user_email_verification_status(user, True)
    login_user(user)
    """redirect to unverified, but show diff ui"""
    return redirect(url_for("protected.dashboard"))


@unprotected.route("/register", methods=["GET", "POST"])
@limiter.limit("10/minute")
@limiter.limit("2/second")
def register():
    register_form = RegisterForm()

    if register_form.validate_on_submit(): #AUTOMATICALLY VALIDATES CSRF
        email = register_form.email.data
        name = register_form.name.data
        surname = register_form.surname.data
        city = register_form.city.data
        un_hashed_password = register_form.password.data
        # un_hashed_password_confirmation = register_form.password_confirm.data

        #CHECK IF USER ALREADY EXIST
        user_exist = get_user_by_email(email)

        if not user_exist:
            #HARSD PASSWORD
            hashed_password = werkzeug.security.generate_password_hash(un_hashed_password, method="scrypt", salt_length=16)
            user = create_new_user(email, name, surname, city, hashed_password)

            login_user(user)
            flash("success", "info")

            #SEND VERIFICATION EMAIL
            token = make_token(email)
            verify_url = url_for("unprotected.verify_email", token=token, _external=True)
            send_mail(verify_url, email)

            return redirect(url_for("protected.unverified")) #CHANGE TO DASHBOARD or unverified
        else:
            flash("User Already Exist", "error")

            return redirect(url_for("unprotected.register"))

    return render_template("register.html", form=register_form)