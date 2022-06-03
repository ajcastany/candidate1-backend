#!/usr/bin/python3
import configparser
import psycopg2
from typing import Dict, List
from flask import Flask
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

def db_conn():
    db_dict = read_config("db_conn.config")
    conn = psycopg2.connect(dbname=db_dict['db'], host=db_dict['host'],
                            user=db_dict['username'], password=db_dict['password'], port=db_dict['port'])
    print("conn success!!")
    conn.close()
    print("Connection terminated!")

"""
MAIN
"""

app = Flask(__name__)
conf_dict = read_config("db_conn.config")
app.config.update(
    ENV='development',
    SQLALCHEMY_DATABASE_URI=conf_dict['server_uri'],
    SQLALCHEMY_TRACK_MODIFICATIONS= False
    )

db = SQLAlchemy(app)
    
@app.route('/api', methods=['GET'])
def TEST():
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0')
