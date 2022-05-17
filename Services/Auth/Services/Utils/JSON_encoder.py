# Helps to encode objects containing datetime and UUID (and others if added)
# Usage: json.dumps(obj, default = json_encoder)

import datetime
import json
from uuid import UUID

from bson import ObjectId


def json_encoder(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, UUID):
        return str(obj)
    if isinstance(obj, datetime.date) or isinstance(obj, datetime.datetime):
        return obj.isoformat()


def json_recode(obj):
    st = json.dumps(obj, default=json_encoder)
    return json.loads(st)
