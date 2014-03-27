import datetime
import json
import yaml
import os.path

import timegrapple.util as util

import __main__

FILE_PATH = "%s/sheets/%s_week_%s.%s"
_ROOT = __main__._ROOT


def load(when=None):
    if isinstance(when, basestring):
        when = util.string_to_date(when)
    if when is None:
        when = datetime.date.today()

    generate_file(when)

    data = load_file(when)
    today = when.strftime("%Y-%m-%d")
    return data[today]


def save(when, day):
    if isinstance(when, basestring):
        when = util.string_to_date(when)
    if when is None:
        raise Exception("need to specify a day to save for")

    data = load_file(when)

    data[day['id']] = day

    save_file(data, when)


def load_file(when=None, style='yaml'):
    if when is None:
        when = datetime.date.today()
    (year, week_num, day_num) = when.isocalendar()

    filename = FILE_PATH % (_ROOT, year, week_num, style)

    if not os.path.exists(filename):
        raise Exception("can't load the file")

    stream = file(filename, 'r')
    if style == 'json':
        return json.load(stream)
    elif style == 'yaml':
        return yaml.load(stream)


def save_file(data, when, output='yaml'):
    filename = get_filename(when, output)

    stream = file(filename, 'w')
    if output == 'json':
        json.dump(data, stream, sort_keys=True,
                  indent=2, separators=(',', ': '))
    elif output == 'yaml':
        yaml.safe_dump(data, stream, default_flow_style=False)


def get_filename(when, output='yaml'):
    (year, week_num, day_num) = when.isocalendar()

    return FILE_PATH % (_ROOT, year, week_num, output)


def generate_file(when=None, output='yaml'):
    if when is None:
        when = datetime.date.today()

    (year, week_num, day_num) = when.isocalendar()

    filename = get_filename(when, output)
    if os.path.exists(filename):
        return "already exists"

    # http://www.tutorialspoint.com/python/python_date_time.htm
    # filename is "%s_week_%s.json"
    days = util.get_days(year, week_num)
    hours = range(7, 21)

    data = {}
    for d in days:
        day = {}
        key = d.strftime("%Y-%m-%d")

        yesterday, tomorrow = util.tomorrow_yesterday(d)

        data[key] = day
        date_pretty = util.pretty_num(d.day)
        day['name'] = "%s %s" % (d.strftime("%A %B"), date_pretty)
        day['id'] = key
        day['tomorrow'] = tomorrow
        day['yesterday'] = yesterday
        day['hours'] = []
        for h in hours:
            day['hours'].append({'hour': h, 'value': ''})

    save_file(data, when, output)
