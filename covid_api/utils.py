import json
import enum
import datetime
from contextlib import contextmanager
import decimal

import pytz


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


def json_dumps(d):
    json_str = json.dumps(d, cls=CustomJSONEncoder)
    return clean_unicode_string(json_str)
