import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    DB_HOST = "localhost"
    DB_USER = "root"          # 👈 your MySQL username
    DB_PASSWORD = "Vikas123456"       # 👈 your MySQL password
    DB_NAME = "lost_found_db"  # 👈 your database name

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)