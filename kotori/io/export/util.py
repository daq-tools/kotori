# -*- coding: utf-8 -*-
# (c) 2016-2021 Andreas Motl <andreas.motl@elmyra.de>
from twisted.logger import Logger, LogLevel
log = Logger()


try:
    import pandas
except ImportError:
    log.failure('Dataframe functions not available, please install "pandas".', level=LogLevel.warn)


try:
    from pandas.tslib import Timedelta
except ImportError:
    try:
        from pandas import Timedelta
    except ImportError:
        log.failure('Dataframe functions not available, please install "pandas".', level=LogLevel.warn)


def dataframe_index_to_column(df, column):
    """
    Copy DataFrame index column to real data column.
    """
    dt = df.index
    df[column] = dt
    #df.reset_index(drop=True, inplace=True)
    return df


def dataframe_wide_to_long_indexed(df, column):
    """
    Convert DataFrame from wide to long format using specified column as index column,
    followed by indexing the DataFrame on the very same column and finally sorting it.

    See also:

    - http://pandas.pydata.org/pandas-docs/stable/reshaping.html#reshaping-by-melt
    - http://stackoverflow.com/questions/17688155/complicated-for-me-reshaping-from-wide-to-long-in-pandas
    """
    df = pandas.melt(df, id_vars=column).dropna()
    df = dataframe_index_and_sort(df, column)
    return df


def dataframe_index_and_sort(df, column):
    """
    Index and sort DataFrame on specified column.
    """
    df = df.set_index([column])
    df = df.sort_index()
    return df


def matplotlib_locator_formatter(timedelta, span=1):
    """
    Compute appropriate locator and formatter for renderers
    based on matplotlib, depending on designated time span.
    """
    from matplotlib.dates import DateFormatter
    locator, formatter = date_ticker_factory(span)

    # http://pandas.pydata.org/pandas-docs/stable/timedeltas.html
    # https://stackoverflow.com/questions/16103238/pandas-timedelta-in-days
    is_macro = timedelta <= Timedelta(days=1)
    is_supermacro = timedelta <= Timedelta(minutes=5)

    if is_macro:
        #formatter = DateFormatter(fmt='%H:%M:%S.%f')
        formatter = DateFormatter(fmt='%H:%M')

    if is_supermacro:
        formatter = DateFormatter(fmt='%H:%M:%S')

        # Formatter overrides
        #if formatter.fmt == '%H:%M\n%b %d':
        #    formatter = DateFormatter(fmt='%Y-%m-%d %H:%M')

    # Labs
    #from matplotlib.dates import AutoDateLocator, AutoDateFormatter, HOURLY
    #locator = AutoDateLocator(maxticks=7)
    #locator.autoscale()
    #locator.intervald[HOURLY] = [5]
    #formatter = AutoDateFormatter(breaks)
    #formatter = date_format('%Y-%m-%d\n%H:%M')

    # Default building blocks
    #from matplotlib.dates import AutoDateFormatter, AutoDateLocator
    #locator = AutoDateLocator()
    #formatter = AutoDateFormatter(locator)

    return locator, formatter


def date_ticker_factory(span, tz=None, numticks=5):
    """
    Create a date locator with *numticks* (approx) and a date formatter
    for *span* in days.  Return value is (locator, formatter).

    `date_ticker_factory` was removed from matplotlib in version 3.8.0.
    The recommendation is to use AutoDateLocator and AutoDateFormatter,
    or to vendorize the code.

    https://matplotlib.org/stable/api/prev_api_changes/api_changes_3.8.0.html#date-ticker-factory-removed
    https://github.com/matplotlib/matplotlib/blob/v3.7.5/lib/matplotlib/dates.py#L1784C1-L1823C30
    """
    import math
    from matplotlib.dates import (
        DAYS_PER_MONTH, DAYS_PER_WEEK, DAYS_PER_YEAR, HOURS_PER_DAY, MINUTES_PER_DAY,
        DateFormatter, DayLocator, HourLocator, MinuteLocator, MonthLocator, WeekdayLocator, YearLocator)

    if span == 0:
        span = 1 / HOURS_PER_DAY

    mins = span * MINUTES_PER_DAY
    hrs = span * HOURS_PER_DAY
    days = span
    wks = span / DAYS_PER_WEEK
    months = span / DAYS_PER_MONTH      # Approx
    years = span / DAYS_PER_YEAR        # Approx

    if years > numticks:
        locator = YearLocator(int(years / numticks), tz=tz)  # define
        fmt = '%Y'
    elif months > numticks:
        locator = MonthLocator(tz=tz)
        fmt = '%b %Y'
    elif wks > numticks:
        locator = WeekdayLocator(tz=tz)
        fmt = '%a, %b %d'
    elif days > numticks:
        locator = DayLocator(interval=math.ceil(days / numticks), tz=tz)
        fmt = '%b %d'
    elif hrs > numticks:
        locator = HourLocator(interval=math.ceil(hrs / numticks), tz=tz)
        fmt = '%H:%M\n%b %d'
    elif mins > numticks:
        locator = MinuteLocator(interval=math.ceil(mins / numticks), tz=tz)
        fmt = '%H:%M:%S'
    else:
        locator = MinuteLocator(tz=tz)
        fmt = '%H:%M:%S'

    formatter = DateFormatter(fmt, tz=tz)
    return locator, formatter


def make_timezone_unaware(df):
    # Please ensure that datetimes are timezone unaware before writing to Excel.
    # https://github.com/pandas-dev/pandas/pull/27129
    # https://github.com/pandas-dev/pandas/issues/28921
    # https://stackoverflow.com/questions/61802080/excelwriter-valueerror-excel-does-not-support-datetime-with-timezone-when-savin
    # https://github.com/pandas-dev/pandas/issues/7056
    df['time'] = pandas.to_datetime(
        df['time'], utc=True) \
        .dt.tz_convert('UTC') \
        .dt.tz_localize(None)
