import re
import subprocess
import tempfile

WORDS = ["SHUTDOWN", "YES"]

def isValid(text):
    return bool(re.search(r'\bshutdown\b', text, re.IGNORECASE))

def handle(text, mic, profile):
    mic.say("Are you sure?")

    if bool(re.search(r'\byes\b', mic.activeListen(), re.IGNORECASE)):
        mic.say("Shutting down.  Goodbye for now.  It's been real")

        with tempfile.TemporaryFile() as f:
            cmd = ['sudo', 'shutdown', '-h', 'now']
            subprocess.call(cmd, stdout=f, stderr=f)
