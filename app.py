from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail

from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
mail = Mail(app)

login_manager.login_view = 'login'
from routes import *  
from models import *
from forms import *

if __name__ == '__main__':
    app.run(debug=True)
