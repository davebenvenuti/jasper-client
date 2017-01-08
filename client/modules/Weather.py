# -*- coding: utf-8-*-
from subprocess import Popen, PIPE
import re

WORDS = ["WEATHER"]

def handle(text, mic, profile):
    mic.say("just a moment")

    cmd = ["node", "/home/pi/wunderground-cli/weather.js"]
    p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    output, err = p.communicate()
    lines = output.split("\n")
    weather = lines[1]
    temperature = int(round(float(lines[2].split(' F ')[0])))

    mic.say("the current weather is %s.  The temperature is %d degrees" % (weather, temperature))

def isValid(text):
    """
        Returns True if the text is related to the weather.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\b(weathers?|temperature|forecast|outside|hot|' +
                          r'cold|jacket|coat|rain)\b', text, re.IGNORECASE))
