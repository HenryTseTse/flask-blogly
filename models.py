"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class User(db.Model):
    """ User Model """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column(db.Text, nullable = False)
    last_name = db.Column(db.Text, nullable = False)
    image_url = db.Column(db.Text, nullable = True, default="")

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

class Post(db.Model):
    """ Post Model """

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.Text, nullable = False)
    content = db.Column(db.Text, nullable = False)
    created_at = db.Column(
        db.DateTime,
        nullable = False,
        default = datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

def connect_db(app):
    """Connect to DB"""

    db.app = app
    db.init_app(app)