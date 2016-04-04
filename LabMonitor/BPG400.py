# Inficon BPG400 Pressure sensor RS232 Protocol
# 9600, stop bit, no parity bit

# From pump
# Pump sends a 9-byte string without request approx every 20ms
# The whole output frame is 9 bytes.
# First and last bytes are frame metadata.
# <length (7), page number (5), status, error, measurement hi,
# measurement low, software version, sensor type (10), checksum>
# Status byte:
# <emission, emission, adjustment, message count parity,
# pressure unit, pressure unit, not used, not used>
# Error byte:
# <not used, not used, not used, not used,
# err, err, err, err>
# Software version:
# decimal = byteValue / 20
# Pressure:
#  mbar: 10^((hi*256 + lo)/4000-12.5)
#  torr: 10^((hi*256 + lo)/4000-12.625)
#  pa: 10^((hi*256 + lo)/4000-10.5)
# Checksum:
# Sum bytes 1-7 (not length byte). Mod 256

# To pump
# Five byte string
# <length (3), data, data, data, checksum>

import serial

class BPG400(object):
    """Class for BPG400 pressure sensor"""
    def __init__(self, serialPortPath):
        """BPG400("/dev/correctSerialPort")"""
        self.path = serialPortPath
        self.serial = serial.Serial(serialPortPath, 9600)
    def synchronize(self):
        """bpg400.synchronize()
        Wait for a whole message to come through the serial line.
        """
        while True:
            while ord(self.serial.read()) != 7: # Wait for start byte
                pass
            if ord(self.serial.read()) != 5: # Page number
                continue # Try again
            data = bytearray(self.serial.read(5))
            if ord(self.serial.read()) != 10: # Sensor type
                continue # Try again
            checksum = ord(self.serial.read())
            if checksum != (5 + sum(data) + 10) % 256:
                raise Exception("Bad checksum during synchronize")
            return
    def read(self):
        """bpg400.read() Returns a BPG400_Measurement"""
        self.serial.reset_input_buffer()
        self.serial.synchronize()
        packet = bytearray(self.serial.read(9))
        return parse_packet(packet)

def parse_packet(packet):
    if packet[0] != 7:
        raise Exception("Invalid length byte")
    if packet[1] != 5:
        raise Exception("Invalid page number")
    status = packet[2]
    error = packet[3]
    hi = packet[4]
    lo = packet[5]
    ver = packet[6]
    if packet[7] != 10:
        raise Exception("Invalid sensor type")
    checksum = packet[8]
    if checksum != sum(packet[1:8]) % 256:
        raise Exception("Bad checksum")
    return BPG400_Measurement(status, error, hi, lo, ver)

class BPG400_Measurement(object):
    """Has the following methods:
    version() returns the version of the sensor.
    mbar() returns pressure in mbar.
    torr() returns pressure in torr.
    pa() returns pressure in pascals.
    status() returns a string representation of the sensor status
    error() returns a string rep of the sensor's error state
        or None if there is no error.
    """
    def __init__(self,status,err,hi,lo,ver):
        self.stat = status
        self.err = err & 240
        self.hi = hi
        self.lo = lo
        self.raw = float((hi * 256) + lo)
        self.ver = ver
    def version(self):
        return self.ver / 20.0
    def mbar(self):
        return 10**(self.raw/4000 - 12.5)
    def torr(self):
        return 10**(self.raw/4000 - 12.625)
    def pa(self):
        return 10**(self.raw/4000 - 10.5)
    def status(self):
        emission = {
            0: "off",
            1: "25uA",
            2: "5mA",
            3: "Degas"
        }[self.stat & 3]
        adj = {0:"off", 1:"on"}[self.stat & (1<<2)]
        unit = {0:"mbar", 1:"torr", 2:"pa"}[self.stat & 48]
        return "Emission {}, 1000 mbar adjustment {}, on-screen unit {}"\
            .format(emission, adj, unit)
    def error(self):
        errors = {
            (1 << 6) + (1 << 4) : "Pirani adjusted poorly",
            (1 << 7)            : "BA error (What does BA stand for?)",
            (1 << 7) + (1 << 4) : "Pirani error"
        }
        if self.err in errors:
            return errors[self.err]
        else:
            return None
