# -*- coding: utf-8 -*-
"""
Created on Wed Aug  12 11:36:05 2020

@author: harshit-saraswat
"""

from datetime import datetime
try:
    from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
except ImportError:
    from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from flaskblog import db, loginManager

try:
    from flask_login import UserMixin
except ImportError:
    from flaskblog.mock_extensions import UserMixin


@loginManager.user_loader
def load_user(userID):
    return User.query.get(int(userID))

class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), unique=True, nullable=False)
    email=db.Column(db.String(120), unique=True, nullable=False)
    image_file=db.Column(db.String(20), nullable=False, default="default.jpg")
    password=db.Column(db.String(60), nullable=False)
    posts=db.relationship('Post', backref='author', lazy=True)
    reviews=db.relationship('Review', backref='reviewer', lazy=True)

    def get_reset_token(self,expires_sec=1800):
        s=Serializer(current_app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id=s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    date_posted=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content=db.Column(db.Text, nullable=False)
    image_file=db.Column(db.String(20), nullable=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reviews=db.relationship('Review', backref='post', lazy=True, cascade='all, delete-orphan')

    def get_average_rating(self):
        """Calculate average rating for this post"""
        if self.reviews:
            total_rating = sum(review.rating for review in self.reviews)
            return round(total_rating / len(self.reviews), 1)
        return 0

    def get_rating_count(self):
        """Get total number of reviews for this post"""
        return len(self.reviews)

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text, nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"Review('{self.rating}', '{self.date_posted}')"
