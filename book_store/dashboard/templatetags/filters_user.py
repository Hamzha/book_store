import datetime
from time import strftime, gmtime

from django import template
from django.utils import timezone

register = template.Library()


@register.filter(name='times')
def times(number):
    return range(number)


@register.filter(name='times_reverse')
def times_reverse(number):
    print(range(number))
    rangeTmp =(range(number)[0], range(number)[1]-5)
    print(rangeTmp)
    return rangeTmp


@register.filter(name='calculate_price')
def calculate_price(price, percentage):
    after_price = price - price * (percentage / 100)
    return after_price


@register.filter(name='expire_time')
def expire_time(time):
    print('time', type(time))
    time = datetime.date.strftime(time, "%m/%d/%Y")
    return time


@register.filter(name='time_format')
def time_format(time):
    time = strftime("%H:%M:%S", gmtime(time))

    return time


@register.filter(name='calculate_years')
def calculate_years(date_of_birth):
    print(type(date_of_birth))
    print(type(datetime.datetime.now()))
    try:
        diff = datetime.datetime.now(timezone.utc) - date_of_birth
        print((diff.seconds / (365.25 * 24 * 60 * 60)))
        return diff.seconds / (365.25 * 24 * 60 * 60)
    except Exception as e:
        print(e)
    return 12
