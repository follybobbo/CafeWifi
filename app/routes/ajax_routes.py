from app import create_flask_app
from app.services import (check_if_user_can_resend_verification_email, redis_client, make_token, send_mail,
                          get_single_cafe_by_cafe_name, update_status_of_cafe_to_opened_closed, get_review_record_using_id,
                          update_review_summary, get_all_cafes_and_order_by_id, get_all_cafe_instance_by_location, update_user_display_picture)
from app.Utils import is_photo_file_allowed
from flask_login import current_user, login_required
from flask import url_for, jsonify, Blueprint, request, session, flash, redirect, make_response
from werkzeug.utils import secure_filename
import requests
from dotenv import load_dotenv
import os



load_dotenv()


app = create_flask_app()

ajax_rule = Blueprint("ajax", __name__)
GOOGLE_PLACES_API_KEY = os.environ.get("API")
ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg"]








@ajax_rule.route("/resend-verification", methods=["POST"])
def resend_verification_email():
    can_send_the_mail = check_if_user_can_resend_verification_email(current_user.id, redis_client)

    if can_send_the_mail:
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
@ajax_rule.route("/restaurant/closed-or-opened", methods=["PATCH"])
def report_closed_or_opened():
    request_body = request.get_json()
    restaurant_name = request_body.get("name")
    restaurant_to_update = get_single_cafe_by_cafe_name(restaurant_name)

    status = restaurant_to_update.status

    #close or open restaurant
    result = update_status_of_cafe_to_opened_closed(restaurant_to_update, status)
    return result


#USES RESTAURANT NAME FROM FRONTEND TO CHECK THE OPEN STATUS FROM THE DB
@ajax_rule.route("/restaurant/status", methods=["GET"])
def check_restaurant_status():
    restaurant_name = request.args.get("name")
    db_restaurant = get_single_cafe_by_cafe_name(restaurant_name)

    if db_restaurant:
        status = db_restaurant.status
        if status:
            return jsonify({"status": True})
        else:
            return jsonify({"status": False})



#UPDATES SUMMARY VALUE IN DB, RETURNS STATUS WHEN DONE
@app.route("/update/summary", methods=["PATCH"])
def update_summary():
    request_body = request.get_json()
    name_of_restaurant = request_body.get("name")
    summary_value = request_body.get("summary_value")


    #GET DB TO UPDATE
    restaurant_to_update = get_single_cafe_by_cafe_name(name_of_restaurant)
    restaurant_id = restaurant_to_update.id

    #GET REVIEW DATABASE
    review_db = get_review_record_using_id(restaurant_id)
    # review_db = db.session.execute(db.select(Review).where(Review.id == restaurant_id)).scalar()

    #UPDATE DB
    update_review_summary(review_db, summary_value)

    return jsonify({"status": "updated"})


#USES GOOGLE API TO SEARCH FOR USERS CITY USING LONGITUDE AND LATITUDE used in index.js
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
        cafe_instance = get_all_cafes_and_order_by_id()
        restaurants = cafe_instance.all()

    for restaurant in restaurants:
        list_of_places.append({"name": restaurant.name, "city": restaurant.city})

    return list_of_places


#view searches through db and gets result for latitude and longitude in list used in show-venue.js
@app.route("/api/latlong")
def get_lat_and_long():
    lat_long_list = []
    city = request.args.get("city")
    cafe_instance = get_all_cafe_instance_by_location(city)
    result = cafe_instance.all()

    for restaurant in result:
        latitude = restaurant.latitude
        longitude = restaurant.longitude

        lat_long_list.append({"lat": latitude, "lng": longitude, "title": restaurant.name})


    return lat_long_list  #returns list of latitude and longitude of each location

@app.route("/change-display-picture", methods=["POST", "GET"])
def change_display_picture():
    if request.method == "POST":

        #structure of request.files :
        # ImmutableMultiDict([
        #   ('name_on_input', <FileStorage: 'image_name or filename', ('image/jpg or MIME type')>)
        # ])

        # if request has no file: hence form field does not have name = file
        if "photo" not in request.files:
            flash("No file part In Form", "error")
            return redirect(request.url)

        file = request.files.get("photo")
        if file.filename == "":
            flash("No File Selected", "error")
            return redirect(request.url)


        if file and is_photo_file_allowed(file.filename, ALLOWED_EXTENSIONS):
            print(current_user)
            folder = f"./static/uploads/users/{current_user.id}"
            #make folder per user
            os.mkdir(folder)

            #store file in users folder
            filename = secure_filename(file.filename)
            path = os.path.join(folder, filename)


            try:
                file.save(path)
            except Exception as e:
                flash(f"An Error Occurred: {e}", "info")
            else:
                update_user_display_picture(current_user.id, path)












# @app.route("/api/get-backoff", methods=["POST", "GET"])
# def get_time_for_backoff():
#     print(request.method)
#     # request_body = request.get_json()
#     # user_email = request_body.get("user_email")
#     user_email = request.args.get("email")
#     print(user_email)
#
#     user_key = f"auth:login:{user_email}:cooldown"
#
#     print(f"get_time_for_backoff {user_key}")
#     user_exist : bool
#
#     user_exist = redis_client.exists(user_key)
#     print(f"get_time_for_backoff {user_exist}")
#
#     if user_exist:
#         time_remaining = redis_client.ttl(user_key)
#
#         return jsonify({"is_back_off": True, "result": time_remaining})
#     else:
#         return jsonify({"is_back_off": False, "result": 0})                 # can change later

