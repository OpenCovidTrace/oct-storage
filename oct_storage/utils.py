import json
import enum
import datetime
import calendar
from contextlib import contextmanager
import decimal

import pytz

EPOCH_DT = datetime.datetime.utcfromtimestamp(0).replace(tzinfo=pytz.UTC)


@contextmanager
def precision_context(precision):
    yield decimal.localcontext(decimal.Context(prec=precision))


def utcnow():
    return datetime.datetime.utcnow().replace(tzinfo=pytz.utc)


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        elif isinstance(obj, datetime.time):
            return obj.strftime('%H:%M')
        elif isinstance(obj, enum.Enum):
            return obj.value
        elif isinstance(obj, enum.AutoNameEnum):
            return obj.name
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(CustomJSONEncoder, self).default(obj)


def json_obj(*args, **kwargs):
    """Dump json object with encoding of custom types"""
    return json_dumps(dict(*args, **kwargs))


def clean_unicode_string(val):
    cl_val = val.replace(r'\u0000', '')
    return cl_val


def json_dumps(obj):
    json_str = json.dumps(obj, cls=CustomJSONEncoder)
    return clean_unicode_string(json_str)


def datetime_to_timestamp_ms(dt):
    return (dt - EPOCH_DT).total_seconds() * 1000.0


def datetime_to_timestamp(dt):
    return calendar.timegm(dt.utctimetuple())


def date_to_timestamp(date):
    return datetime_to_timestamp(datetime.datetime(date.year, date.month, date.day))


class AutoNameEnum(enum.Enum):
    '''Makes auto enum value equal to key'''
    def _generate_next_value_(name, start, count, last_values):
        return name
