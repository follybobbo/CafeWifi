from app import create_flask_app
from app.extensions import db

app = create_flask_app()


with app.app_context():
    db.create_all()
    print("Database created")