from typing import List, Optional
import datetime
import decimal

from pydantic import BaseModel, validator
from . import utils


class DayItem(datetime.date):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, int):
            raise TypeError('day in int type required')
        dt = utils.day_number_to_date(v)
        return cls(dt.year, dt.month, dt.day)


class UserKey(str):
    pass


class Latitude(decimal.Decimal):
    pass


class Longitude(decimal.Decimal):
    pass


class Border(BaseModel):
    minLat: Latitude
    maxLat: Latitude
    minLng: Longitude
    maxLng: Longitude


class TrackFilter(Border):
    lastUpdateTimestamp: Optional[datetime.datetime]


class KeyFilter(TrackFilter):
    pass


class Meta(str):
    pass


class KeyItem(BaseModel):
    day: DayItem
    value: UserKey
    border: Border
    meta: Optional[Meta]


class KeysBlock(BaseModel):
    keys: List[KeyItem]

    @validator('keys')
    def min_keys(cls, vals):
        if not vals:
            raise ValueError('must contain items')
        return vals


class Point(BaseModel):
    tst: datetime.datetime
    lng: decimal.Decimal
    lat: decimal.Decimal


class Track(BaseModel):
    key: UserKey
    day: DayItem
    points: List[Point]

    @validator('points')
    def min_points(cls, vals):
        if not vals:
            raise ValueError('must contain items')
        return vals


class TracksBlock(BaseModel):
    tracks: List[Track]

    @validator('tracks')
    def min_tracks(cls, vals):
        if not vals:
            raise ValueError('must contain items')
        return vals
