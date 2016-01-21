#!/usr/bin/python3
#*-*Coding: UTF-8 *-*
__author__ = "fnjeneza"

import datetime
import random

def work_hour():
    """
    generate a random work hour
    work hour is gauss distribution.
    9:00 - 12:00, mean is 10:30
    14:00 - 17:00, mean is 15:30
    sigma= 1h
    """
    #date planned
    date_planned = datetime.datetime.today()

    # 4:50 PM
    five_pm = datetime.datetime.today().replace(hour=16,minute=50,second=00)
    # current date
    now = datetime.datetime.today()
    # time left, in seconds, before 5:0 PM
    time_left = (five_pm-now).total_seconds()

    #if less than 10 min left before 5:00 PM
    #report to the day after
    if time_left < 0:
        date_planned = date_planned+datetime.timedelta(days=1)

    # if the planned/current day is weekend
    # report to monday
    weekday = date_planned.weekday()
    if not 0<=weekday<=4:
        date_planned = date_planned+datetime.timedelta(
                days=7-weekday)


    while True:
        hour,minute = _schedule()
        # schedule date
        sched = date_planned.replace(hour=hour,minute=minute)
        # timedelta
        delta = sched-now
        if (delta.days>0
                or (delta.days==0 and delta.seconds>0)):
            date_planned = sched
            return date_planned.timestamp()


def _schedule():
    """
    generate a time between 9:00 - 12:00 or 14:00 - 17:00
    choice is "am" or "pm", default is None
    return an tuple (hour, minute)
    """
    while True:
        # random choice mean 10:30 => 36030 in seconds
        # or mean 15:30 => 54030 in seconds
        mean = random.choice([36030,54030])
        # gaussian random
        # sigma 1h => 3600 in seconds
        sigma = 3600
        rtime = int(random.gauss(mean,sigma))
        hour = int(rtime/3600)
        minute = int(rtime%3600)%60

        if (9<=hour<12 or 14<=hour<17):
            return hour,minute

