import geoalchemy2 as ga

from .app import db
from . import utils


class Track(db.Model):
    __tablename__ = 'tracks'

    id = db.Column(db.String(50), primary_key=True)
    user_id = db.Column(db.BigInteger(), index=True, nullable=False)
    linestring = db.Column(ga.Geometry('MultiPointZ'))
    created = db.Column(db.DateTime(timezone=True), default=utils.utcnow)
