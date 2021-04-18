from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMG_URL = "https://i.pinimg.com/originals/70/99/df/7099dfba8504d5a3cbbea9558876bff0.jpg"


def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Models for Blogly."""

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

    def __repr__(self):
        """Show info about user.""" 
        u = self
        return f"<Pet {u.id} {u.first_name} {u.last_name} {u.image_url}>"

    @property
    def full_name(self):
        """Return full name of user."""
        return f"{self.first_name} {self.last_name}"
                

