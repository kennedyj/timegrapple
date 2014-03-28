import datetime
import isoweek


def pretty_num(n):
    end = "th"
    if 4 <= n % 100 <= 20:
        end = "th"
    else:
        end = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return str(n) + end


def date_generator(from_date, count=7):
    for x in range(0, count):
        yield from_date
        from_date = from_date + datetime.timedelta(days=1)


def get_days(year, week):
    # week == weeknum
    start = isoweek.Week(year, week).monday()

    return [d for d in date_generator(start)]


def tomorrow_yesterday(today):
    if isinstance(today, basestring):
        today = string_to_date(today)

    delta = datetime.timedelta(days=1)

    yesterday = date_to_string(today - delta)
    tomorrow = date_to_string(today + delta)

    return (yesterday, tomorrow)


def string_to_date(when):
    return datetime.datetime.strptime(when, "%Y-%m-%d").date()


def date_to_string(date):
    return date.strftime("%Y-%m-%d")


def get_mondays(year=2014):
    delta = datetime.timedelta(days=7)
    monday = isoweek.Week(year, 1).monday()

    days = []
    while monday.year <= year:
        days.append(monday)
        monday = monday + delta

    return days
