""" Debug function """
import os
import json
import pkgutil
import sys

def debug_handler(event, context):
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
  
