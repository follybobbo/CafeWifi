from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from app.services import (get_all_cafes_and_order_by_id, get_cafe_city_list, get_all_cafe_instance_by_location,
                          get_all_cafe_and_order_by_country, create_country_city_list_dictionary, get_user_by_email,
                          de_serializer, update_user_email_verification_status, create_new_user, make_token, send_mail,
                          remove_certain_keys_session, BackOff, redis_client, check_if_session_key_is_expired,
                          remove_singular_key_from_session)
from dotenv import load_dotenv
import os
from app import cache, limiter
from app.decorators import login_token_bucket_limiter
from flask_login import login_user, logout_user
from app.forms import LoginForm, RegisterForm
import werkzeug.security
import time


load_dotenv()



unprotected = Blueprint("unprotected", __name__)
GOOGLE_PLACES_API_KEY = os.environ.get("API")
back_off = BackOff(redis_client)




#ROUTES
@unprotected.route("/")
@limiter.limit("10/minute")
@limiter.limit("2/second")
@cache.cached(timeout=50)
def home():

    # print(request.url)
    #Reads DB and stores location in list, conditional statement ensures there is no repetition of location
    list_of_key = ["csrf_token", "location_name", "picture_url", "country", "city", "street_name", "longitude", "latitude", "step"]
    remove_certain_keys_session(list_of_key)
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



@unprotected.route("/city/<location>")
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
    #make sure cooldown only shows when user makes a get request
    login_form = LoginForm()
    # failed_login = False
    # print(session.get("expiry_time"), "expiry")
    # print(time.time())

    # 1 the cooldown key had already been set to expire after 3600 seconds in redis, the block of code below tracks that for the front end.
    # 2 the expiry time has been set below at the moment the user makes the first failed attempt using (time of first
    #   failure attempt + 3600) since the key expires 3600s after first creation
    # 3 so on every get request to this route, the first thing that happens is to check if the key has expired
    is_ttl_session_key_expired = check_if_session_key_is_expired("expiry_time")

    #if key has expired in redis which is our main backend tracker/reinforcer, then the key is deleted from session
    if is_ttl_session_key_expired:
        remove_singular_key_from_session("expiry_time")

    if session.get("redirect"):
        session["redirect"] = False
    else:
        session["ttl"] = None



    if login_form.validate_on_submit():

        email = login_form.email.data
        password = login_form.password.data
        user = get_user_by_email(email)

        user_backoff_key = f"auth:login:{user}"
        user_cooldown_key = f"auth:login:{user}:cooldown"
        #get if user is banned

        #runs if user email supplied does not exist
        if not user:
            #back off here
            flash("Invalid Credentials", "error")
            return  redirect(url_for("unprotected.register"))

        #check if user entered has previously attempted a failed login and has be set to cooldown.
        # this is where cooldown state is determined, not in redis
        if redis_client.exists(user_cooldown_key):
            time_remaining = redis_client.ttl(user_cooldown_key)
             # x = redis_client.ttl(user_cooldown_key)
            session["ttl"] = time_remaining
            print(session.get("ttl"))

            session["redirect"] = True
            flash(f"you can't login now try again in {time_remaining}s", "error")
            return redirect(url_for("unprotected.login"))



        #check if blocked: send to account recovery/verification
        #This will only run if user exist.
        is_password = werkzeug.security.check_password_hash(user.password, password)

        if not is_password:
            #runs script to register failed login attempt and register cooldown
            failed_attempt, delay = back_off.start_back_off(user_backoff_key)

            if failed_attempt == 10:
                pass
                #ban user
                #make write action to db.banned

            # create id and count
            #check subsequently, if user try 3 times give a cool off timer of 3 mins, 3 more times, 6 mins, then one more block off


            flash(f"Invalid Details wait for {delay}s", "error")
            #original delay, set here
            session["ttl"] = delay
            print(session.get("ttl"))
            session["expiry_time"] = time.time() + 3600
            session["redirect"] = True

            return redirect(url_for("unprotected.login"))
        else:
            flash("Login Success", "info")
            login_user(user)
            #delete user from black list and removes timer from session.
            back_off.delete_black_list_record(user_backoff_key)
            session.pop("ttl")

            return redirect(url_for("protected.dashboard"))



    return render_template("login.html", form=login_form, cooldown_time=session.get("ttl", None))


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