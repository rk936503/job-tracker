from app import app
from extensions import db
from models import User

with app.app_context():
    username = input("Username: ")
    password = input("Password: ")

    existing = User.query.filter_by(username=username).first()
    if existing:
        print("That username already exists.")
    else:
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print(f"User '{username}' created successfully.")
