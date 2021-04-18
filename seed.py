"""Seed file to make sample data for pets db."""

from models import User, db
from app import app

TEST_IMG_URL = "https://media.distractify.com/brand-img/JC3OTI_vP/0x0/monkey-pfp-1597428196891.jpeg"

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
john = User(first_name='John', last_name="Smith")
sasha = User(first_name='Sasha', last_name="Klevchuk", image_url=TEST_IMG_URL)
lena = User(first_name='Lena', last_name="Klevchuk")


# Add new objects to session, so they'll persist
db.session.add(john)
db.session.add(sasha)
db.session.add(lena)

# Commit--otherwise, this never gets saved!
db.session.commit()
