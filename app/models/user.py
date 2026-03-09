# from sqlalchemy.orm import Mapped, mapped_column
# from sqlalchemy import String, DateTime
# from flask_login import UserMixin
# from datetime import datetime
# from app.extensions import db
#
# class User(db.Model, UserMixin):
#     __tablename__ = "user"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
#     name: Mapped[str] = mapped_column(String(500), nullable=False)
#     surname: Mapped[str] = mapped_column(String(500), nullable=False)
#     city: Mapped[str] = mapped_column(String(500), nullable=False)
#     password: Mapped[str] = mapped_column(nullable=False)
#     verified: Mapped[bool] = mapped_column(nullable=False, default=False)
#     opened: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow())
