import json
from bson import json_util


def convertToJson(data):
    return json.dumps(data, default=json_util.default)
