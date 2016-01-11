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

    # current date and time
    now = datetime.datetime.today()
    
    #date planned
    date_planned = now

    # 5:0 PM
    five_pm = date_planned.replace(hour=17,minute=00,second=00)
    # time left, in seconds, before 5:0 PM
    time_left = (five_pm-date_planned).total_seconds()

    #if less than 2 min left before 5:00 PM
    #report to the day after
    if time_left < 120:
        date_planned = date_planned+datetime.timedelta(days=1)

    # if the planned/current day is weekend
    # report to monday
    weekday = date_planned.weekday()
    if not 0<=weekday<=4:
        date_planned = date_planned+datetime.timedelta(
                days=7-weekday)

    # if planned at current date
    if date_planned == now:
        hour_planned = date_planned.hour
        minute_planned = date_planned.minute
        if hour_planned < 9:
            hour_planned, minute_planned = _schedule('am')

        if 12 <hour_planned <14:
            hour_planned, minute_planned = _schedule('pm')

        date_planned = date_planned.replace(hour=hour_planned,
            minute=minute_planned)
    # if planned another day
    else:
        hour_planned, minute_planned = _schedule()

        date_planned = date_planned.replace(hour=hour_planned,
            minute=minute_planned)

    # date_planned in seconds
    return date_planned.timestamp()


def _schedule(choice=None):
    """
    generate a time between 9:00 - 12:00 or 14:00 - 17:00
    choice is "am" or "pm", default is None
    return an tuple (hour, minute)
    """
    if choice is None:
        choice = random.choice(['am','pm'])
    
    hour = 0
    minute = 0
    if choice=='am':
        #gauss distribution between 9 and 12
        while not 9 <hour<12:
            # mean 10:30,=> 36030 in seconds
            # sigma is 1 hour,=> 3600 in seconds
            rtime  = int(random.gauss(36030,3600))
            hour = int(rtime/3600)
            minute = (rtime%3600)%60
    else:
        # gauss distribution between 14 and 17
        while not 14<hour<17:
            # mean 15:30,=> 54030 in seconds
            # sigma is 1 hour,=> 3600 in seconds
            rtime  = int(random.gauss(54030,3600))
            hour = int(rtime/3600)
            minute = (rtime%3600)%60

    return hour, minute
