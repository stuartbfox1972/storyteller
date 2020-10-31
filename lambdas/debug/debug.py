""" Debug function """
from __future__ import unicode_literals
import os
import json
import pkgutil
import sys

class PythonObjectEncoder(json.JSONEncoder):
    """Custom JSON Encoder that allows encoding of un-serializable objects
    For object types which the json module cannot natively serialize, if the
    object type has a __repr__ method, serialize that string instead.
    Usage:
        >>> example_unserializable_object = {'example': set([1,2,3])}
        >>> print(json.dumps(example_unserializable_object,
                             cls=PythonObjectEncoder))
        {"example": "set([1, 2, 3])"}
    """

    def default(self, obj):
        if isinstance(obj, (list, dict, str, int, float, bool, type(None))):
            return json.JSONEncoder.default(self, obj)
        elif hasattr(obj, '__repr__'):
            return obj.__repr__()
        else:
            return json.JSONEncoder.default(self, obj.__repr__())

def debug_handler(event, context):
  """ Entry point """
  mods = []
  for p in pkgutil.iter_modules():
    mods.append(p[1])
  cxt = json.dumps(vars(context), cls=PythonObjectEncoder)
  response = {'ENV': dict(**os.environ),
              'EVENT': event,
              'CONT': cxt,
              'MODS': mods,
              'SUB': event['requestContext']['authorizer']['jwk']['claims']['sub']
             }

  return json.dumps(response)

