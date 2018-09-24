
from .base import *
import os
import json



def str_to_bool(s):
    if s == 'True':
        return True
    elif s == 'False':
        return False
    else:
        raise ValueError


try:
    if str_to_bool(os.environ['DJANGO_IS_PRODUCTION']):
        from .production import *
except:
    with open("secretsLocal.json") as f:
        secrets = json.loads(f.read())
        if str_to_bool(secrets["CONFIG_SISTEMA"]['DJANGO_IS_LOCAL']):
            from .local import *