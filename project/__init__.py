from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman
import os 

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()
migrate = Migrate()
csrf = CSRFProtect()
talisman = Talisman()

def create_app():
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sql12436225:9V4TUBB2NZ@sql12.freemysqlhosting.net/sql12436225'
  app.config['SECRET_KEY'] = 'ems_medical_standby'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
  app.config['MAIL_PORT'] = 587
  app.config['MAIL_USE_TLS'] = True
  app.config['MAIL_USERNAME'] = 'pps.etdhtaa@gmail.com'
  app.config['MAIL_PASSWORD'] = "PPSetdht@@"
  app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
  app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.pdf','.jpeg', '.JPG']
  app.config['UPLOAD_PATH'] = 'project/static/'

  db.init_app(app)

  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)

  jwt.init_app(app)
  mail.init_app(app)
  migrate.init_app(app,db)
  csrf.init_app(app)
  talisman.init_app(app, content_security_policy=None)

  from .models import User, OAuth, Events

  @login_manager.user_loader
  def load_user(user_id):
    return User.query.get(int(user_id))

  #blueprints auth routes
  from .auth import auth as auth_blueprint
  app.register_blueprint(auth_blueprint.auth)

  #non-auth parts
  from .calendar import calendar as calendar_blueprint
  app.register_blueprint(calendar_blueprint.calendar)

  return app