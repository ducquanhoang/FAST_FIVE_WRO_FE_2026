# Python Library for MATRIX Line Tracer 10CH
# Author : Anthony Hsu
# Date   : 2026.04.18, For Firmware ver 101, 201

# !! Upload this file into your Pybricks editor !! 

from pybricks.iodevices import PUPDevice
from pybricks.parameters import Port

# ════════════════════════════════════════════════════════════════
#  Class（Full Functions）
# ════════════════════════════════════════════════════════════════

class MXLineTracer:
    JUNCTION_NAMES = {0: "none", 1: "left", 2: "right", 3: "T/cross"}

    _DEFAULT_WEIGHTS = (-4.5, -3.5, -2.5, -1.5, -0.5,
                         0.5,  1.5,  2.5,  3.5,  4.5)


    def __init__(self, port, threshold=30):
        self._dev = PUPDevice(port)
        self._threshold = threshold
        self._weights = list(self._DEFAULT_WEIGHTS)

    def set_weights(self, *weights):
        if len(weights) != 10:
            raise ValueError("Need 10 weights!")
        self._weights = list(weights)

    def set_threshold(self, threshold):
        self._threshold = threshold

    def _read(self):
        return self._dev.read(1)

    def sensors(self):
        p = self._read()
        out = []
        for i in range(5):
            out.append((p[i] >> 8) & 0xFF)
            out.append( p[i]       & 0xFF)
        return out

    def error(self, sensors=None):
        if sensors is None:
            sensors = self.sensors()
        weighted_sum = 0.0
        total_weight = 0.0
        for i in range(10):
            if sensors[i] < self._threshold:
                w = self._threshold - sensors[i]
                weighted_sum += w * self._weights[i]
                total_weight += w
        return 0.0 if total_weight == 0 else weighted_sum / total_weight

    def bitmap(self):
        return self._read()[5]

    def on_sensors(self):
        bm = self.bitmap()
        return [i + 1 for i in range(10) if bm & (1 << i)]

    def on_line(self):
        return bool((self._read()[6] >> 5) & 0x1)

    def line_width(self):
        return (self._read()[6] >> 6) & 0xF

    def last_sensor(self):
        return (self._read()[6] >> 10) & 0xF

    def junction(self):
        return (self._read()[6] >> 14) & 0x3

    def junction_name(self):
        return self.JUNCTION_NAMES[self.junction()]

    def version(self):
        return self._read()[7]

    def read_all(self):
        p = self._read()
        sensors = []
        for i in range(5):
            sensors.append((p[i] >> 8) & 0xFF)
            sensors.append( p[i]       & 0xFF)
        bm = p[5]
        p6 = p[6]
        return {
            "sensors":     sensors,
            "bitmap":      bm,
            "on_sensors":  [i + 1 for i in range(10) if bm & (1 << i)],
            "on_line":     bool((p6 >> 5) & 0x1),
            "line_width":  (p6 >> 6) & 0xF,
            "last_sensor": (p6 >> 10) & 0xF,
            "junction":    (p6 >> 14) & 0x3,
            "version":     p[7],
            "error":       self.error(sensors),
        }


# ════════════════════════════════════════════════════════════════
#  Flat functions（For Blockly, bridge via global _mxlt）
# ════════════════════════════════════════════════════════════════

_mxlt = None   # global MXLineTracer instance

def lt_init(port_letter):
    global _mxlt
    port = eval('Port.' + port_letter)
    _mxlt = MXLineTracer(port)

def lt_set_threshold(threshold):
    _mxlt.set_threshold(threshold)

def lt_set_weights(w1, w2, w3, w4, w5, w6, w7, w8, w9, w10):
    _mxlt.set_weights(w1, w2, w3, w4, w5, w6, w7, w8, w9, w10)

def lt_sensors():
    return _mxlt.sensors()

def lt_error():
    return _mxlt.error()

def lt_on_line():
    return _mxlt.on_line()

def lt_line_width():
    return _mxlt.line_width()

def lt_last_sensor():
    return _mxlt.last_sensor()

def lt_junction():
    return _mxlt.junction()

def lt_version():
    return _mxlt.version()