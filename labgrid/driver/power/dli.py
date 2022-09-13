import re
import subprocess
import requests

def power_set(host, port, index, value):
    value = 'on' if value else 'off'
    ret = subprocess.run(['p4', 'set', index, value])
    if ret.returncode:
        raise Exception()

def power_get(host, port, index):
    ret = subprocess.run(['p4', 'get', index], capture_output=True)
    if ret.returncode:
        raise Exception()

    return ret.stdout.strip().endswith(b'ON')
