from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
DATABASE_URL = os.environ["DATABASE_URL"]

