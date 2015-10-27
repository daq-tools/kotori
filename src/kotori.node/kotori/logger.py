# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>

# from mqtt.logger
from twisted.logger   import (
    LogLevel, globalLogBeginner,
    FileLogObserver, FilteringLogObserver, LogLevelFilterPredicate,
    formatTime, timeFormatRFC3339, formatEvent)

def startLogging(fileobj, level=LogLevel.debug):
    fileObserver = logObserver(fileobj)
    predicate    = LogLevelFilterPredicate(defaultLogLevel=level)
    observers    = [ FilteringLogObserver(observer=fileObserver, predicates=[predicate]) ]
    globalLogBeginner.beginLoggingTo(observers)


# overwritten from twisted.logger

def logObserver(outFile, timeFormat=timeFormatRFC3339):
    def formatEvent(event):
        return formatLogEvent(
            event, formatTime=lambda e: formatTime(e, timeFormat)
        )

    return FileLogObserver(outFile, formatEvent)


def formatLogEvent(event, formatTime=formatTime):
    eventText = formatEvent(event)
    if not eventText:
        return None

    eventText = eventText.replace(u"\n", u"\n\t")
    timeStamp = formatTime(event.get("log_time", None))

    system = event.get("log_system", None)

    if system is None:
        level = event.get("log_level", None)
        if level is None:
            levelName = u"-"
        else:
            levelName = level.name

        system = u"{namespace}".format(
            namespace=event.get("log_namespace", u"-"),
        )
    else:
        try:
            system = unicode(system)
        except Exception:
            system = u"UNFORMATTABLE"

    return u"{timeStamp} [{system}] {level}: {event}\n".format(
        timeStamp=timeStamp,
        system=system.ljust(33),
        level=levelName.upper(),
        event=eventText,
    )


__all__ = [startLogging]
