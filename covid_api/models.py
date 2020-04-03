import geoalchemy2 as ga

from .app import db
from . import utils, constants


class Track(db.Model):
    __tablename__ = 'tracks'

    id = db.Column(db.BigInteger(), primary_key=True)
    user_id = db.Column(db.BigInteger(), index=True, nullable=False)
    geo_points = db.Column(ga.Geometry('MultiPointZ'))
    created = db.Column(db.DateTime(timezone=True), default=utils.utcnow)
    health_status = db.Column(
        db.Enum(constants.HealthStatus, name='health_status_enum'),
        default=constants.HealthStatus.covid_confirmed
    )
