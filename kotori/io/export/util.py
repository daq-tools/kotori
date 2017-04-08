# -*- coding: utf-8 -*-
# (c) 2016 Andreas Motl <andreas.motl@elmyra.de>
from twisted.logger import Logger, LogLevel
log = Logger()

try:
    import pandas
    from pandas.tslib import Timedelta
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
    from matplotlib.dates import date_ticker_factory, DateFormatter
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

