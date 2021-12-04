import datetime
from time import strftime, gmtime

from django import template
from django.utils import timezone
from datetime import date
import time

register = template.Library()


@register.filter(name='times')
def times(number):
    return range(number)


@register.filter(name='times_reverse')
def times_reverse(number):
    rangeTmp =(range(number)[0], range(number)[1]-5)
    return rangeTmp


@register.filter(name='calculate_price')
def calculate_price(price, percentage):
    after_price = price - price * (percentage / 100)
    return after_price


@register.filter(name='expire_time')
def expire_time(time):
    time = datetime.date.strftime(time, "%m/%d/%Y")
    return time


@register.filter(name='time_format')
def time_format(time):
    time = strftime("%H:%M:%S", gmtime(time))

    return time


@register.filter(name='calculate_years')
def calculate_years(date_of_birth):
    print(type(date_of_birth))
    try:
        diff = datetime.datetime.now() - date_of_birth.replace(tzinfo=None)
        return diff.days / 365
    except Exception as e:
        print(e)
    return 12
