#!/usr/bin/python3
import sys
import configparser
from dataclasses import dataclass
from operator import itemgetter
import psycopg2
from typing import Dict, List
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import false

"""
VARIABLES
"""

conn_dict = dict()

"""
FUNCTIONS
"""


def read_config(file_path):
    dictionary = dict()
    # if more than 1 section is needed, create a dict of dicts
    dict_list = list()
    config = configparser.ConfigParser()
    config.read(file_path)
    for section in config.sections():
        for key in config[section]:
            dictionary[key] = config[section][key]
    return (dictionary)


"""
DEF
"""

""" def db_conn():
    db_dict = read_config("db_conn.config")
    conn = psycopg2.connect(dbname=db_dict['db'], host=db_dict['host'],
                            user=db_dict['username'], password=db_dict['password'], port=db_dict['port'])
    print("conn success!!")
    conn.close()
    print("Connection terminated!")
 """
"""
MAIN
"""

app = Flask(__name__)
conf_dict = read_config("db_conn.config")
app.config.update(
    ENV='development',
    SQLALCHEMY_DATABASE_URI=conf_dict['server_uri'],
    SQLALCHEMY_TRACK_MODIFICATIONS= False,
    JSON_SORT_KEYS = False
    )


db = SQLAlchemy(app)

"""
Models:
"""
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
    fk = db.relationship('DailyForm', lazy='dynamic')
            
    
@dataclass
class DailyForm(db.Model):
    __tablename__ = "daily_form"
    
    id: int
    day: db.DATE
    name: int
    room: str
    time_in: db.TIME
    time_out: db.TIME
    tag: str
    tag_ret: bool
    
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.DATE, nullable=False)
    name = db.Column(db.Integer, db.ForeignKey('staff.id' ), nullable=False)
    room = db.Column(db.String, nullable=True)
    time_in = db.Column(db.TIME, nullable=True)
    time_out = db.Column(db.TIME, nullable=True)
    tag = db.Column(db.String, nullable=True)
    tag_ret = db.Column(db.Boolean, nullable=True)
    

"""
Routes:
"""
    
@app.route('/api/staff/all', methods=['GET'])
def all_staff():
    test = Staff.query.all()
    return jsonify(test)

@app.route('/api/staff/<id>', methods=['GET'])
def staff(id):
    try:
        staff = Staff.query.filter_by(id=id).first()
        return jsonify(staff)
    except:
        return ("resource not found")

@app.route('/api/daily_form/<day>', methods=['GET'])
def daily_form(day):
    try:
        day_form = DailyForm.query.join(Staff, DailyForm.name==Staff.id)\
            .add_columns(Staff.name, Staff.department).filter(day==DailyForm.day).all()
        form_tup = [tuple(row) for row in day_form]
        print(day, file=sys.stderr)
        return jsonify(form_tup)
    except:
        return "Resource not found"
    
@app.route('/api/all_days')
def all_days():
    day_form = DailyForm.query.join(Staff, DailyForm.name==Staff.id)\
    .add_columns(Staff.name, Staff.department).all()
    form_tup = [tuple(row) for row in day_form]
        
    return jsonify(form_tup)
        
        

if __name__ == '__main__':
    app.run(host='0.0.0.0')
