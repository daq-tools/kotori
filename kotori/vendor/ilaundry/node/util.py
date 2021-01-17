# -*- coding: utf-8 -*-
# (c) 2014 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import os
import sys
import urllib.parse


def tts_say(message, language='de'):

    # FIXME: add queue here
    print("say:", message)

    # Google Translate TTS
    # FIXME: urlescape "message"
    tts_url = u'http://translate.google.com/translate_tts?tl={language}&q={message}'.format(language=language, message=urllib.parse.quote(message.encode('utf8')))
    more_args = u''
    if sys.platform.startswith('linux'):
        # TODO: dynamic configuration of output device
        more_args += u'-ao alsa:device=hw=1.0'

    user_agent = u"-http-header-fields 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'"
    command = u"mplayer -really-quiet -noconsolecontrols {user_agent} {more_args} '{tts_url}'".format(**locals())
    #command = command.encode('utf8')
    print(command)
    # FIXME: don't do this synchronously
    # FIXME: show errors (stdout/stderr) if command fails
    os.system(command)
