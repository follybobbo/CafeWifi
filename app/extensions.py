from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address




class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
limiter = Limiter(
        get_remote_address,
        default_limits=["10 per minute"],
        storage_uri="redis://localhost:6379/2",
        strategy="fixed-window"
    )