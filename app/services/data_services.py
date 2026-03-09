


def get_data_dict_for_show_location(review_instance):
    data_dict = {

        "PRODUCTIVITY": {
            # display_text: [tooltip_text, data_for_review]
            "stable wifi": ["is there wifi", review_instance.wifi],
            "power sockets": ["Is it easy to find power sockets", review_instance.power_sockets],
            "length of work": ["How long can you comfortably stay and work ?", review_instance.length_of_work],
            "tables and chairs": ["Are tables and chairs comfortable for work ?", review_instance.tables_and_chairs],
            "is it quiet": ["Is it quiet ?", review_instance.is_it_quiet],
            "audio and video": ["Can you comfortably make audio/video calls ?", review_instance.audio_and_video]
        },
        "COMMUNITY": {
            "people working": ["Is it common to see other people working ?", review_instance.other_people_working],
            "group tables": ['Are there group tables (for 6+ people)', review_instance.group_tables]
        },
        "SERVICE": {
            "coffee": ["Is coffee available", review_instance.coffee_available],
            "food": ["Is food offered", review_instance.food_offered],
            "veggie": ["Are there veggie options", review_instance.veggie_options],
            "Alcohol": ["Is alcohol offered", review_instance.alcohol_offered],
            "credit cards": ["Are credit cards accepted ?", review_instance.credit_cards]
        },
        "SPACE": {
            "Natural light": ["Is the space full of natural light", review_instance.natural_light],
            "Outdoor area": ["Is there an outdoor area?", review_instance.outdoor_area],
            "Spacious": ["How large is the place ?", review_instance.how_large],
            "Restroom": ["Is there a restroom", review_instance.restroom],
            "Accessible": ["Is it easily accessible with a wheelchair", review_instance.wheelchair_accessible],
            "Air conditioned": ["Is the place air conditioned ?", review_instance.air_conditioned],
            "Smoke free": ["Is the space smoke free", review_instance.smoke_free],
            "Pet friendly": ["Is it pet friendly", review_instance.pet_friendly],
            "Parking": ["Is there a parking space", review_instance.parking_space]
        }
    }

    return data_dict