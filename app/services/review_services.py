from app.models import Review
from app.extensions import db
from flask import jsonify


def write_record_to_review_db(wifi, power_sockets, length_of_work, tables_and_chairs, is_it_quiet, audio_and_video,
                              other_people_working, group_tables, coffee_available, food_offered, veggie_options,
                              alcohol_offered, credit_cards, natural_light, outdoor_area, how_large,
                              restroom, wheelchair_accessible, air_conditioned, smoke_free, pet_friendly, parking_space,
                              summary, restaurant_id):

    review_record = Review(
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
        restaurant_id=restaurant_id
    )

    db.session.add(review_record)
    db.session.commit()


def get_review_record_using_id(id_of_cafe):
    review_record = db.session.execute(db.select(Review).where(Review.restaurant_id == id_of_cafe)).scalar()

    return review_record


def update_review_record(review_db_instance, wifi, power_sockets, length_of_work, tables_and_chairs, is_it_quiet,
                         audio_and_video, other_people_working, group_tables, coffee_available, food_offered,
                         veggie_options, alcohol_offered, credit_cards, natural_light, outdoor_area, how_large, restroom,
                         wheelchair_accessible, air_conditioned, smoke_free, pet_friendly, parking_space, summary):


    review_db_instance.wifi = wifi
    review_db_instance.power_sockets = power_sockets
    review_db_instance.length_of_work = length_of_work
    review_db_instance.tables_and_chairs = tables_and_chairs
    review_db_instance.is_it_quiet = is_it_quiet
    review_db_instance.audio_and_video = audio_and_video
    review_db_instance.other_people_working = other_people_working
    review_db_instance.group_tables = group_tables
    review_db_instance.coffee_available = coffee_available
    review_db_instance.food_offered = food_offered
    review_db_instance.veggie_options = veggie_options
    review_db_instance.alcohol_offered = alcohol_offered
    review_db_instance.credit_cards = credit_cards
    review_db_instance.natural_light = natural_light
    review_db_instance.outdoor_area = outdoor_area
    review_db_instance.how_large = how_large
    review_db_instance.restroom = restroom
    review_db_instance.wheelchair_accessible = wheelchair_accessible
    review_db_instance.air_conditioned = air_conditioned
    review_db_instance.smoke_free = smoke_free
    review_db_instance.pet_friendly = pet_friendly
    review_db_instance.parking_space = parking_space
    review_db_instance.summary = summary


    db.session.commit()

    return jsonify({"Info": "Update Successful"}), 200


def update_review_summary(review_db_instance, value_of_summary):
    review_db_instance.summary = value_of_summary
    db.session.commit()

