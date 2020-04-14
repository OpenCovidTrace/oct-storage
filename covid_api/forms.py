from typing import List, Optional
import datetime
import decimal

from pydantic import BaseModel, validator


class DayItem(datetime.date):
    pass


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


class KeyItem(BaseModel):
    day: datetime.date
    value: UserKey
    border: Border


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
