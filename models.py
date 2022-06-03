#!/usr/bin python3

from dataclasses import dataclass
from time import time
from psycopg2 import Time

from sqlalchemy import TIME, ForeignKey, true
from main import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

@dataclass
class Staff(db.Model):
    """From an answer on SO: https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json"""
    __tablename__  = "staff"
    
    id: int
    name: str
    department: str
    
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    
@dataclass
class DailyForm(db.model):
    __tablename__ = "daily_form"
    
    id: int
    name: str
    room: str
    time_in: TIME
    time_out: TIME
    tag: str
    tag_ret: bool
    
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    name = db.relationship('Staff', ForeignKey("staff.id"))
    room = db.Column(db.String, nullable=True)
    time_in = db.Column(db.TIME, nullable=True)
    time_out = db.Column(db.TIME, nullable=True)
    tag = db.Column(db.String, nullable=True)
    tag_ret = db.Column(db.Bool, nullable=True)
