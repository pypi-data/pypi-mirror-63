#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2018-2020, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
from pytz import BaseTzInfo
from tzlocal import get_localzone

from doccron.job import Job


class InvalidSchedule(Exception):
    pass


class CronTable(object):

    # noinspection PyShadowingNames
    def __init__(self, jobs, quartz=False):
        self._jobs = {}
        self._previous_schedule = None
        self._timezone = get_localzone()
        for j in jobs:
            if isinstance(j, BaseTzInfo):
                self._timezone = j
                continue
            try:
                job = Job(j, quartz=quartz, timezone=self._timezone)
            except ValueError:
                raise InvalidSchedule
            self._jobs[job] = next(job)

    def __iter__(self):
        return self

    # noinspection PyShadowingNames
    def __next__(self):
        if not len(self._jobs):
            return
        job, next_schedule = sorted(self._jobs.items(), key=lambda x: x[1])[0]
        if next_schedule is None:
            del self._jobs[job]
            return
        self._jobs[job] = next(job)
        if self._previous_schedule and next_schedule <= self._previous_schedule:
            return next(self)
        self._previous_schedule = next_schedule
        return next_schedule

    next = __next__
