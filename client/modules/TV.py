from subprocess import Popen, PIPE
import re
import signal
import os

WORDS = ["ROW", "COO", "CHROMECAST", "EX", "BOX", "NETFLIX"]

def isValid(text):
    return _isRoku(text) or _isXbox(text) or _isChromecast(text) or _isNetflix(text)

def handle(text, mic, profile):
    wakeTV()

    if _isRoku(text):
        mic.say("turning on row coo")

        _run(['nodejs', '/home/pi/lgcontrol/lgcontrol.js', 'set_input', 'HDMI_1'])

    elif _isXbox(text):
        mic.say("turning on ex box")

        _run(['nodejs', '/home/pi/lgcontrol/lgcontrol.js', 'set_input', 'HDMI_2'])
        _run(['/usr/local/bin/turn-on-xbox'])

    elif _isChromecast(text):
        mic.say("turning on chrome cast")

        _run(['nodejs', '/home/pi/lgcontrol/lgcontrol.js', 'set_input', 'HDMI_3'])

    elif _isNetflix(text):
        mic.say("turning on netflix")

        _run(['nodejs', '/home/pi/lgcontrol/lgcontrol.js', 'set_input', 'HDMI_1'])
        _run(['nodejs', '/home/pi/roku-control/rokucontrol.js', 'launch', 'netflix'])

def _isRoku(text):
    return bool(re.search(r'\brow\b', text, re.IGNORECASE)) and bool(re.search(r'\bcoo\b', text, re.IGNORECASE))

def _isXbox(text):
    return bool(re.search(r'\bex\b', text, re.IGNORECASE)) or bool(re.search(r'\bbox\b', text, re.IGNORECASE))

def _isChromecast(text):
    return bool(re.search(r'\bchromecast\b', text, re.IGNORECASE))

def _isNetflix(text):
    return bool(re.search(r'\bnetflix\b', text, re.IGNORECASE))


class Alarm(Exception):
    pass

def alarm_handler(signum, frame):
    raise Alarm

def wakeTV():
    _run(["wakeonlan", "-i", os.environ['TV_IP'], os.environ['TV_MAC']])

def _run(cmdArray, timeout=15):
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(timeout)

    p = Popen(cmdArray, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    out, err = p.communicate()
    signal.alarm(0)
    return out, err
