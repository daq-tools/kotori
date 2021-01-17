# -*- coding: utf-8 -*-
# (c) 2015-2021 Andreas Motl <andreas@getkotori.org>
import re


class MessageType:

    DATA_DISCRETE = 1
    DATA_CONTAINER = 2
    EVENT = 3
    ERROR = 4


class TopicPatterns:

    data = [

        # Legacy v1 (deprecated)
        'message-json',

        # En bloc
        '/data.json',

        # Homie
        'data/__json__',

        # WeeWX
        'loop',

    ]

    discrete = [
        # Discrete value
        # {base}/data/temperature
        '/(data|measure)/[^/]+',
    ]

    event = [

        # Record of event data
        'event.json',

        # Homie support
        'event/__json__',
    ]

    error = [

        # Error data arrives on this suffix
        'error.json',
    ]

    @classmethod
    def compile_patterns(cls, patterns):
        matcher = re.compile('({parts})'.format(parts='|'.join([x + '$' for x in patterns])))
        return matcher


class TopicMatchers:
    data = TopicPatterns.compile_patterns(TopicPatterns.data)
    discrete = TopicPatterns.compile_patterns(TopicPatterns.discrete)
    event = TopicPatterns.compile_patterns(TopicPatterns.event)
    error = TopicPatterns.compile_patterns(TopicPatterns.error)
