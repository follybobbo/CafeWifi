from flask import jsonify
from app.extensions import db

def create_country_city_list_dictionary(cafe_instance_country_ordered, dictionary_storage: dict):
    for rows in cafe_instance_country_ordered:
        # assigns country to var
        country = rows.country

        # gets list of country in city_dict
        country_list = dictionary_storage.keys()

        # if currently looped country is present in country_list
        if country in country_list:
            # gets its city list
            city_list = dictionary_storage.get(country)
            # if city is not in city list then add city to city list. this condition is to prevent duplicate city being added
            if rows.city not in city_list:
                city_list.append(rows.city)
        else:
            dictionary_storage[country] = [rows.city]


    return dictionary_storage


def get_cafe_city_list(cafe_instance, city_list: list):
    for rows in cafe_instance:
        location = rows.city
        #TO AVOID REPETITION OF LOCATION
        if location not in city_list:
            city_list.append(location)


    return city_list


def update_status_of_cafe_to_opened_closed(restaurant_to_update, status):
    if status:
        restaurant_to_update.status = False
        db.session.commit()

        return jsonify({"status": "closed"})
    else:
        restaurant_to_update.status = True
        db.session.commit()

        return jsonify({"status": "opened"})

