import pyvisa
import time

from pathlib import Path


class BK91xx:
    def __init__(self, uri, channel, baudrate=38400):
        try:
            self.res = pyvisa.ResourceManager('@py').open_resource(uri)
        except Exception:
            raise ConnectionError

        self.channel = channel
        self.res.baud_rate = baudrate
        self.res.read_termination = '\n'
        self.res.write_termination = '\n'

    def __enter__(self):
        self.res.write('system:remote')
        active_ch = int(self.res.query('instrument:nselect?'))
        if active_ch != self.channel:
            self.res.write(f'instrument:nselect {self.channel}')
        return self.res

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.res.write('system:local')
        self._flush_errors()
        self.res.close()

    def _flush_errors(self):
        errors = list()
        while True:
            ret, msg = self.res.query('system:error?').split(',')
            if int(ret) == 0:
                break

            errors.append((int(ret), msg.strip()))

        if len(errors):
            raise RuntimeError(errors)


def power_set(host, port, index, value):
    index = int(index)
    value = 1 if value else 0
    assert index in [1, 2, 3]

    with BK91xx(uri=host, channel=index) as psu:
        psu.write(f'channel:output {value}')


def power_get(host, port, index):
    index = int(index)
    assert index in [1, 2, 3]

    with BK91xx(uri=host, channel=index) as psu:
        ret = psu.query('channel:output?')

    return int(ret)
