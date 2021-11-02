import datetime
from time import strftime, gmtime

from django import template

register = template.Library()


@register.filter(name='times')
def times(number):
    return range(number)


@register.filter(name='calculate_price')
def calculate_price(price, percentage):
    after_price = price - price * (percentage / 100)
    return after_price


@register.filter(name='expire_time')
def expire_time(time):
    print('time', type(time))
    time  = datetime.date.strftime(time, "%m/%d/%Y")
    return time


@register.filter(name='time_format')
def time_format(time):
    time = strftime("%H:%M:%S", gmtime(time))

    return time

