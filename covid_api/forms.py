from typing import List, Optional
import datetime
import decimal

from pydantic import BaseModel, validator

from . import constants


class TrackFilter(BaseModel):
    timestamp: Optional[datetime.datetime]
    lastUpdateTimestamp: Optional[datetime.datetime]
    radius: Optional[int]
    lng: Optional[decimal.Decimal]
    lat: Optional[decimal.Decimal]


class Point(BaseModel):
    tst: datetime.datetime
    lng: decimal.Decimal
    lat: decimal.Decimal


class Track(BaseModel):
    userId: int
    healthStatus: Optional[constants.HealthStatus]
    points: List[Point]

    @validator('points')
    def min_points(cls, vals):
        if not vals:
            raise ValueError('must contain items')
        return vals
