"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

DEFAULT_IMG_URL = "https://i.pinimg.com/originals/70/99/df/7099dfba8504d5a3cbbea9558876bff0.jpg"


def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Model for User."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True
                    )
    first_name = db.Column(db.String(50),
                            nullable=False
                            )
    last_name = db.Column(db.String(50),
                            nullable=False
                            )
    image_url = db.Column(db.String(50),
                            nullable=False,
                            default = DEFAULT_IMG_URL
                            )

    posts = db.relationship( 'Post', backref='user')
    

    def __repr__(self):
        """Show info about user.""" 
        u = self
        return f"<Pet {u.id} {u.first_name} {u.last_name} {u.image_url}>"

    @property
    def full_name(self):
        """Return full name of user."""
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """Model for Post."""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True
                    )
    title = db.Column(db.Text,
                            nullable=False
                            )
    content = db.Column(db.Text,
                            nullable=False
                            )
    created_at = db.Column(db.DateTime,
                            nullable=False,
                            default=datetime.datetime.now
                            )
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)





                

