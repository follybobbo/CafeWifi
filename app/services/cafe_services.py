from app.models import Cafe
from app.extensions import db


def get_all_cafes_and_order_by_id():
    cafe = db.session.execute(db.select(Cafe).order_by(Cafe.id)).scalars()

    return cafe

def get_all_cafe_and_order_by_country():
    cafe = db.session.execute(db.select(Cafe).order_by(Cafe.country)).scalars()
    return cafe



def query_db_and_filter_by(filter_value: str):
    cafe_instance = Cafe.query.filter_by(
        name=filter_value
    ).first()
    return cafe_instance

def get_all_cafe_instance_by_location(location: str):
    cafe_list_instance = db.session.execute(db.select(Cafe).where(Cafe.city == location)).scalars()

    return cafe_list_instance


def get_single_cafe_by_cafe_name(name_of_cafe: str):
    cafe_row_instance = db.session.execute(db.select(Cafe).where(Cafe.name == name_of_cafe)).scalar()

    return cafe_row_instance


def write_new_cafe(name:str, image_url:str, city:str, address:str, latitude:str, longitude:str, country:str, status:bool):
    new_cafe = Cafe(
        name=name,
        img_url=image_url,
        city=city,
        address=address,
        latitude=latitude,
        longitude=longitude,
        country=country,
        status=status
    )
    db.session.add(new_cafe)
    db.session.commit()