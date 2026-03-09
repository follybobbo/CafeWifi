# from app.extensions import db
# from sqlalchemy.orm import Mapped, mapped_column, relationship
# from sqlalchemy import String, ForeignKey
# from app.models.cafe import Cafe
#
#
#
# class Review(db.Model):
#     __tablename__ = "review"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     wifi: Mapped[str] = mapped_column(String(250), nullable=False)
#     power_sockets: Mapped[str] = mapped_column(String(250), nullable=False)
#     length_of_work: Mapped[str] = mapped_column(String(250), nullable=False)
#     tables_and_chairs: Mapped[str] = mapped_column(String(250), nullable=False)
#     is_it_quiet: Mapped[str] = mapped_column(String(250), nullable=False)
#     audio_and_video: Mapped[str] = mapped_column(String(250), nullable=False)
#
#     other_people_working: Mapped[str] = mapped_column(String(250), nullable=False)
#     group_tables: Mapped[str] = mapped_column(String(250), nullable=False)
#
#     coffee_available: Mapped[str] = mapped_column(String(250), nullable=False)
#     food_offered: Mapped[str] = mapped_column(String(250), nullable=False)
#     veggie_options: Mapped[str] = mapped_column(String(250), nullable=False)
#     alcohol_offered: Mapped[str] = mapped_column(String(250), nullable=False)
#     credit_cards: Mapped[str] = mapped_column(String(250), nullable=False)
#
#     natural_light: Mapped[str] = mapped_column(String(250), nullable=False)
#     outdoor_area: Mapped[str] = mapped_column(String(250), nullable=False)
#     how_large: Mapped[str] = mapped_column(String(250), nullable=False)
#     restroom: Mapped[str] = mapped_column(String(250), nullable=False)
#     wheelchair_accessible: Mapped[str] = mapped_column(String(250), nullable=False)
#     air_conditioned: Mapped[str] = mapped_column(String(250), nullable=False)
#     smoke_free: Mapped[str] = mapped_column(String(250), nullable=False)
#     pet_friendly: Mapped[str] = mapped_column(String(250), nullable=False)
#     parking_space: Mapped[str] = mapped_column(String(250), nullable=False)
#
#     summary: Mapped[str] = mapped_column(String(250), nullable=False)
#
#
#     restaurant_id: Mapped[int] = mapped_column(ForeignKey("cafe.id"))
#     # input_restaurant: Mapped["Cafe"] = relationship(back_populates="user_review")
#     input_restaurant = db.relationship("Cafe", back_populates="user_review")