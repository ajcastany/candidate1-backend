#!/usr/bin python3

from dataclasses import dataclass
from main import db

@dataclass
class Staff(db.Model):
    """From an answer on SO: https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json"""
    __tablename__  = "staff"
    
    id: int
    name: str
    department: str
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    fk = db.relationship('DailyForm', lazy='dynamic', primaryjoin="DailyForm.name == Staff.id")
            
    
@dataclass
class DailyForm(db.Model):
    __tablename__ = "daily_form"
    
    id: int
    name: int
    room: str
    time_in: db.TIME
    time_out: db.TIME
    tag: str
    tag_ret: bool
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, db.ForeignKey('staff.id' ))
    room = db.Column(db.String, nullable=True)
    time_in = db.Column(db.TIME, nullable=True)
    time_out = db.Column(db.TIME, nullable=True)
    tag = db.Column(db.String, nullable=True)
    tag_ret = db.Column(db.Boolean, nullable=True)
    