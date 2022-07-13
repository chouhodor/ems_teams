import os
from poplib import POP3_PORT
from select import epoll
from unittest import mock
from . import db
from flask_login import UserMixin
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
import jwt
from time import time

user_bookmarks =db.Table('user_bookmarks', 
  db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
  db.Column('events_id', db.Integer, db.ForeignKey('events.id'))
)


class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(100), unique=True)
  password = db.Column(db.String(100))
  username = db.Column(db.String(150))
  bookmarks = db.relationship('Events', secondary=user_bookmarks, backref='bookmark')
  events = db.relationship('Events', backref = 'user', lazy='dynamic')

  def __repr__(self):
      return 'User {}'.format(self.username)

  def get_reset_token(self, expires=500):
    return jwt.encode(
      {'reset_password': self.username, 'exp': time() + expires},
      os.getenv('SECRET_KEY', 'random_key'), algorithm='HS256')

  @staticmethod
  def verify_reset_token(token):
    try:
      username = jwt.decode(token, os.getenv('SECRET_KEY', 'random_key'), 
                              algorithm='HS256')['reset_password']
    except:
      return
    return User.query.filter_by(username = username).first()    

  @staticmethod
  def verify_email(email):
    user = User.query.filter_by(email = email).first()
    return user
  
class OAuth(OAuthConsumerMixin, db.Model):
  __table_args__ = (db.UniqueConstraint("provider", "provider_user_id"),)
  provider_user_id = db.Column(db.String(256), nullable = False)
  provider_user_login = db.Column(db.String(256))
  user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable = False)
  user = db.relationship(User)



class Events(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    startDate = db.Column(db.Date)
    endDate = db.Column(db.Date)
    ephysician = db.Column(db.String(100), nullable=True)
    med_officer = db.Column(db.String(100), nullable=True)
    med_assistant = db.Column(db.String(100), nullable=True)
    snurse = db.Column(db.String(100), nullable=True)
    driver = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(2000), nullable=True)
    file1_id = db.Column(db.String(100), nullable=True)
    created_by = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

