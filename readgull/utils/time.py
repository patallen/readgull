from math import floor


def format_timedelta(timedelta):
    """Takes a timedelta object and returns it as human-readable string"""
    formatted = ""
    mil_left = floor((timedelta).total_seconds() * 1000)
    m = None
    s = None
    if mil_left >= 60000:
        m = floor(mil_left / 60000)
        mil_left = mil_left % 60000
    if mil_left >= 1000:
        s = floor(mil_left / 1000)
        mil = mil_left % 1000
    else:
        mil = mil_left

    if m:
        formatted = "{}m".format(int(m))
    if s:
        formatted = "{} {}s".format(formatted, int(s))
    if mil:
        formatted = "{} {}ms".format(formatted, int(mil))

    return formatted
