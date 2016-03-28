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
        self.synchronize()
    def synchronize():
        """bpg400.synchronize()
        Wait for a whole message to come through the serial line.
        """
        while True:
            while ser.read() != 7: # Wait for start byte
                pass
            if ser.read() != 5: # Page number
                continue # Try again
            data = ser.read(5)
            if ser.read() != 10: # Sensor type
                continue # Try again
            checksum = ser.read()
            if checksum != (5 + sum(data) + 10) % 256:
                raise Exception("Bad checksum during synchronize")
            return
    def read():
        """bpg400.read() Returns a BPG400_Measurement"""
        if ser.read() != 7:
            raise Exception("Invalid length byte")
        if ser.read() != 5:
            raise Exception("Invalid page number")
        status = ser.read()
        error = ser.read()
        hi = ser.read()
        lo = ser.read()
        ver = ser.read()
        if ser.read() != 10:
            raise Exception("Invalid sensor type")
        checksum = ser.read()
        if checksum != (5 + status + error + hi + lo + ver + 10) % 256:
            raise Exception("Bad checksum")
        return BPG400_Measurement(status, error, hi, lo, ver)

class BPG400_Measurement(object):
    def __init__(self,status,error,hi,lo,ver):
        self.status = status
        self.error = error
        self.hi = hi
        self.lo = lo
        self.raw = float((hi * 256) + lo)
        self.ver = ver
    def version():
        return self.ver / 20.0
    def mbar():
        return 10**(self.raw/4000 - 12.5)
    def torr():
        return 10**(self.raw/4000 - 12.625)
    def pa():
        return 10**(self.raw/4000 - 10.5)
