# -*- coding: utf-8 -*-
from django import template
from django.utils.timesince import timesince
import datetime
from django.utils import timezone as djtz


register = template.Library()

def timedelta(value, arg=None):
    if not value:
        return ''
    if arg:
        cmp = arg
    else:
        cmp = djtz.now()
    if value > cmp:
        return u"还有%s" % timesince(cmp,value)
    else:
        return u"%s之前" % timesince(value,cmp)

register.filter('timedelta',timedelta)

def date2timedelta(value, arg=None):
    t = datetime.datetime.combine(value, datetime.time.max).replace(tzinfo=djtz.get_default_timezone())
    
    return timedelta(t, arg)

register.filter('date2timedelta', date2timedelta)
