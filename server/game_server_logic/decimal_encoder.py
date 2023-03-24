# This class allows a Decimal type to be encoded into a JSON object as an int.
# This is necessary because DynamoDB stores Decimal types, not ints.

from decimal import Decimal
import json

class DecimalEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj)
        else:
            return json.JSONEncoder.default(self, obj)