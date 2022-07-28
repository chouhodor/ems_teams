import os
from . import db
from flask_login import UserMixin
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from datetime import date, datetime, timedelta
import jwt
from time import time


class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(100), unique=True)
  password = db.Column(db.String(100))
  username = db.Column(db.String(150))
  role = db.Column(db.String(50), default='viewer')
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
    program = db.Column(db.String(200), nullable=True)
    tarikh = db.Column(db.Date)
    masa = db.Column(db.String(200), nullable=True)
    tempat = db.Column(db.String(200), nullable=True)
    vvip = db.Column(db.String(200), nullable=True)
    ephysician = db.Column(db.String(200), nullable=True)
    med_officer = db.Column(db.String(200), nullable=True)
    med_assistant = db.Column(db.String(200), nullable=True)
    snurse = db.Column(db.String(200), nullable=True)
    driver = db.Column(db.String(200), nullable=True)
    nota = db.Column(db.String(2000), nullable=True)
    file1_id = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(200), default='aktif', nullable=True)
    created_by = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Logs(db.Model):
  __tablename__ = 'logs'
  id = db.Column(db.Integer, primary_key=True)
  program_log = db.Column(db.String(200), nullable=True)
  tarikhmasa_log = db.Column(db.DateTime, default=datetime.utcnow)
  event_change = db.Column(db.String(200), nullable=True)
  changer = db.Column(db.String(100), nullable=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Etdstaff(db.Model):
  __tablename__ = 'etdstaff'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(500), nullable=True)
  jawatan = db.Column(db.String(100), nullable=True)
