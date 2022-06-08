#!/usr/bin/python3
import configparser
from dataclasses import dataclass
from operator import itemgetter
from typing import Dict, List
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON, false

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
MAIN
"""

app = Flask(__name__)
conf_dict = read_config("db_conn.config")
app.config.update(
    ENV='development',
    SQLALCHEMY_DATABASE_URI=conf_dict['server_uri'],
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    JSON_SORT_KEYS=False
)

CORS(app)
db = SQLAlchemy(app)

"""
Models:
"""


@dataclass
class Staff(db.Model):
    """From an answer on SO: https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json"""
    __tablename__ = "staff"

    id: int
    name: str
    department: str

    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    #fk = db.relationship('DailyForm', lazy='dynamic')
    
    def __repr__(self):
        return f"<Staff {staff.id}>"

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
    name = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    room = db.Column(db.String, nullable=True)
    time_in = db.Column(db.TIME, nullable=True)
    time_out = db.Column(db.TIME, nullable=True)
    tag = db.Column(db.String, nullable=True)
    tag_ret = db.Column(db.Boolean, nullable=True)
    staff = db.relationship("Staff")
    
    def __repr__(self):
        return f"<DailyForm {daily_form.id}>"
    
"""
Routes:
"""


@app.route('/')
def home():
    return 'Welcome to the API'


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


@app.route('/api/daily_form/day/<day>', methods=['GET'])
def daily_form(day):
    try:
        day_form = DailyForm.query.join(Staff, DailyForm.name == Staff.id)\
            .add_columns(Staff.name, Staff.department).filter_by(day = DailyForm.day).all()
        form_tup = [tuple(row) for row in day_form]
        return jsonify(form_tup)
    except:
        return "Resource not found"

@app.route('/api/daily_form/row_id/<row_id>', methods=['get'])
def get_day_by_id(row_id):
    try:
        day_form = DailyForm.query.join(Staff, DailyForm.name == Staff.id)\
            .filter(row_id == DailyForm.id).all()
        
        res = dict()

            
        for day in day_form:
            res = {
                "id": day.id,
                "day": day.day,
                "name": day.name,
                "room": day.room,
                "time_in":day.time_in,
                "time_out": day.time_out,
                "tag": day.tag,
                "tag_ret": day.tag_ret,
                "name_dep": {"staff_name": day.staff.name, "staff_dept": day.staff.department}
            }

        print("new dict: " + str(res), flush=True)
        return jsonify(res)
    except Exception as e:
        print("Error: " + str(e), flush=True)


@app.route('/api/daily_form/all_days', methods=['GET'])
def all_days():
    try:
        day_form = DailyForm.query.join(Staff, DailyForm.name == Staff.id).all()
    #print("print" + str(day_form), flush=True)
        res = dict()
        response_list = list()            
        for day in day_form:
            res = {
                "id": day.id,
                "day": day.day,
                "name": day.name,
                "room": day.room,
                "time_in":day.time_in,
                "time_out": day.time_out,
                "tag": day.tag,
                "tag_ret": day.tag_ret,
                "name_dep": {"staff_name:": day.staff.name, "staff_dept": day.staff.department}
            }
            response_list.append(res)
        print("new dict: " + str(response_list), flush=True)
        return jsonify(response_list)
    except Exception as e:
        print("Error: " + str(e), flush=True)
    

@app.route('/api/daily_form/room', methods=['POST'])
def add_room():
    if not request.is_json:
        return "bad request"
    request_json = request.get_json()
    row_id = request_json["id"]
    try:
        daily_form = DailyForm(id=row_id, room=request_json['room'])
        db.session.add(daily_form)
        db.session.commit()
    except:
        return "Bad request"


@app.route('/api/daily_form/time', methods=['POST'])
def time_in_out():
    if not request.is_json:
        return "bad request"
    request_json = request.get_json()
    row_id = request_json['id']
    try:
        daily_form = DailyForm(
            id=row_id, time_in=request_json['time_in'], time_out=request_json['time_out'])
        db.session.add(daily_form)
        db.session.commit()
    except:
        return "bad request"


@app.route('/api/daily_form/tag', methods=['POST'])
def add_tag():
    print("hello", flush=True)
    if not request.is_json:
        print("bad", flush=True)
        return "bad request"
    request_json = request.get_json()
    row_id = request_json['id']
    #print("request", request_json)
    try:
        daily_form = DailyForm.query.filter_by(id=row_id).first()
        daily_form.tag = request_json['tag']
        db.session.add(daily_form)
        # db.session.merge(daily_form)
        db.session.commit()
        return "ok"
    except Exception as e:
        print("bad request: " + str(e), flush=True)
        return "bad request"


@app.route('/api/daily_form/tag_ret', methods=['POST'])
def tag_ret():
    print("tag ret", flush=True)
    if not request.is_json:
        print("bad", flush=True)
        return "bad request"
    request_json = request.get_json()
    row_id = request_json['id']
    print(request_json, flush=True)
    try:
        daily_form = DailyForm(id=row_id, tag_ret=request_json['tag_ret'])
        db.session.add(daily_form)
        db.session.commit()
    except:
        print("bad request", flus=True)
        return "bad request"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
