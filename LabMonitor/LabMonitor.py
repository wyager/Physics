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
