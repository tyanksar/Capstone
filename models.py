import os
from sqlalchemy import Column, String, Integer, create_engine, DateTime
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy.orm import backref
import psycopg2

ENV = 'de'

if ENV == 'dev':
    database_name = "Capstone"
    database_path = "postgres://{}/{}".format(
        'postgres@localhost:5432', database_name)
else:
    database_name = "Capstone"
    database_path = os.environ['DATABASE_URL']
    conn = psycopg2.connect(database_path, sslmode='require')

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
IT Assets

'''


class IT_Assets(db.Model):
    __tablename__ = 'it_assets'

    id = Column(Integer, primary_key=True)
    physical_id = Column(String, nullable=False)
    type = Column(String, nullable=False)
    status = Column(String, nullable=False)

    def __init__(self, physical_id, type, status):
        self.physical_id = physical_id
        self.type = type
        self.status = status

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'physical_id': self.physical_id,
            'type': self.type,
            'status': self.status
        }


'''
Below code is for future enhancement of the
project in which location data is associated with
the IT assets and the users
-------
Location


# class Location(db.Model):
#   __tablename__ = 'location'
#
#   id = Column(Integer, primary_key=True)
#   city = Column(String)
#   building = Column(String)
#   floor = Column (Integer)
#   room = Column (String)
#
#   def __init__(self, city, building, floor, room):
#     self.city = city
#     self.building = building
#     self.floor = floor
#     self.room = room
#
#   def insert(self):
#     db.session.add(self)
#     db.session.commit()
#
#   def update(self):
#     db.session.commit()
#
#   def delete(self):
#     db.session.delete(self)
#     db.session.commit()
#
#   def format(self):
#     return {
#       'id': self.id,
#       'city': self.city,
#       'building': self.building,
#       'floor': self.floor,
#       'room': self.room
#     }
'''


'''
User

'''


class Users(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    badge_no = Column(Integer, nullable=False)

    def __init__(self, name, badge_no):
        self.name = name
        self.badge_no = badge_no

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'badge_no': self.badge_no,
        }


'''
IT asset inventory
'''


class IT_Asset_Inventory (db.Model):
    __tablename__ = 'it_asset_inventory'
    id = db.Column(db.Integer,  primary_key=True)
    it_asset_id = db.Column(db.Integer, db.ForeignKey(
        'it_assets.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), primary_key=True)
    it_assets = db.relationship('IT_Assets', backref=backref(
        "IT_Asset_Inventory", cascade="all,delete"))
    users = db.relationship('Users', backref=backref(
        "IT_Asset_Inventory", cascade="all,delete"))

    def __init__(self, it_asset_id, user_id):
        self.it_asset_id = it_asset_id
        self.user_id = user_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
