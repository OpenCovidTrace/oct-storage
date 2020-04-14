import geoalchemy2 as ga

from .app import db
from . import utils


class Track(db.Model):
    __tablename__ = 'tracks'

    id = db.Column(db.BigInteger(), primary_key=True)
    anon_user_key = db.Column(db.String(80), nullable=False)
    geo_points = db.Column(ga.Geometry('MultiPointZ'))
    date_created = db.Column(db.Date())
    created = db.Column(db.DateTime(timezone=True), default=utils.utcnow)

    geo_boundary = db.Column(ga.Geometry('Polygon'))


class Key(db.Model):
    __tablename__ = 'keys'

    id = db.Column(db.BigInteger(), primary_key=True)
    user_key = db.Column(db.String(80), nullable=False)
    date_created = db.Column(db.Date())
    created = db.Column(db.DateTime(timezone=True), default=utils.utcnow)

    geo_boundary = db.Column(ga.Geometry('Polygon'))
