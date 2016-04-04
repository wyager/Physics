import BPG400
import time

if __name__ == '__main__':
    bpg = BPG400("/dev/ttyUSB0")
    while True:
        time.sleep(0.5) # Just so we don't spam the console.
        print({"{0:.3e} mbar".format(bpg.read().mbar())})