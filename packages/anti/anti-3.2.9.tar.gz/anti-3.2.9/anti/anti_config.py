#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

try:
    from django.conf import settings
except ImportError:
    import config as settings

engine = create_engine(
    settings.ANTI_SQLALCHEMY_DATABASE_URI,
    echo_pool=settings.DEBUG,
    pool_recycle=600
)
session_factory = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
session = scoped_session(session_factory)


### LEGACY ###

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.ANTI_SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)


manager = Manager(app)
manager.add_command('db', MigrateCommand)

class Key(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(255))

class Host(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.String(255))

class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1023))

class Pos(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    date = db.Column(db.Date)
    key_id = db.Column(db.Integer, db.ForeignKey('key.id'))
    host_id = db.Column(db.Integer, db.ForeignKey('host.id'))
    url_id = db.Column(db.Integer, db.ForeignKey('url.id'))
    pos = db.Column(db.SmallInteger)
    search = db.Column(db.SmallInteger)
    lr = db.Column(db.SmallInteger, default=213)

class SeoData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    host_id = db.Column(db.Integer, db.ForeignKey('host.id'))
    tic = db.Column(db.SmallInteger)
    pr = db.Column(db.SmallInteger)
    yaca = db.Column(db.Boolean)
    indexed_google = db.Column(db.Integer)
    indexed_google_clear = db.Column(db.Integer)
    indexed_yandex = db.Column(db.Integer)
    donors = db.Column(db.Integer)
    backlinks = db.Column(db.Integer)
    wm_tic = db.Column(db.Integer)
    wm_indexed = db.Column(db.Integer)

class Visits(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    host_id = db.Column(db.Integer, db.ForeignKey('host.id'))
    av = db.Column(db.Integer)
    rv = db.Column(db.Integer)
    sv = db.Column(db.Integer)

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255))

if __name__ == '__main__':
    manager.run()
