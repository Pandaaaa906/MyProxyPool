# coding=utf-8
import re

import settings


def generate_ip(start_ip, t_range):
    a, b, c, d = re.match('(\d+)\.(\d+)\.(\d+)\.(\d+)', start_ip).groups()
    for i in xrange(t_range):
        yield "{}.{}.{}.{}".format(a, b, c, int(d) + i)


def get_project_settings():
    d = {}
    for key in dir(settings):
        if not key.startswith("__"):
            d[key]=getattr(settings,key)
    return d
