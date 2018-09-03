"""
防止循环引用 建立ORM
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
