from enum import auto

from .utils import AutoNameEnum


class HealthStatus(str, AutoNameEnum):
    healthy = auto()
    feel_sick = auto()
    covid_confirmed = auto()


class TrackLoadStatus(AutoNameEnum):
    new = auto()
    processing = auto()
    loaded = auto()
