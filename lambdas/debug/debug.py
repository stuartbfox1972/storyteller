""" Debug function """
import os
import json
import pkgutil
import sys

def debug(event, context):
  """ Entry point """
  mods = []
  for p in pkgutil.iter_modules():
    mods.append(p[1])
  response = {'ENV': dict(**os.environ),
              'EVENT': event,
              'CONT': context,
              'MODS': mods
             }

  return json.dumps(response)

if __name__ == "__main__":
  print(debug('{"name":"bob"}', '{"age":"21"}'))
