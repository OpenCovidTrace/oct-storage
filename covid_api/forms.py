from typing import List
import datetime
import decimal

from pydantic import BaseModel, validator

from . import constants


class Coord(BaseModel):
    lng: decimal.Decimal
    lat: decimal.Decimal


class Point(BaseModel):
    timestamp: datetime.datetime
    coord: Coord


class Track(BaseModel):
    user_id: int
    health_status: constants.HealthStatus
    points: List[Point]

    @validator('points')
    def min_points(cls, vals):
        if not vals:
            raise ValueError('must contain items')
        return vals
