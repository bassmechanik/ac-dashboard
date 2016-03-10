import os
import sys
import traceback
import ac
import acsys
import platform
import time

def log_error():
    msg = 'Exception: {}\n{}'.format(time.asctime(), traceback.format_exc())
    ac.log(msg)
    ac.console(msg)
    logged_errors.append(msg)

def get_lib_dir():
    if platform.architecture()[0] == '64bit':
        return 'lib64'
    else:
        return 'lib'

# Fix import path for sim_info ctypes
lib_dir = 'apps/python/ArduinoDash/{}'.format(get_lib_dir())
sys.path.insert(0, lib_dir)
os.environ['PATH'] += ';.'

try:
    import serial
except:
    log_error()
    raise

#ser = serial.Serial(3, 9600)
ser = serial.Serial(port = 'COM3', baudrate = 10, timeout = 0)
count = 0
limitisset = 0

def acMain(acVersion):
    # do something with serial library
    global ser
    ac.log("called acMain()")
    time.sleep(3)
    return "Arduino Serial"
def acUpdate(deltaT):
    global limitisset,ser,ac,acsys,count

    if count == 5:
        value=ac.getCarState(0,acsys.CS.RPM)
        value = str(round(value))
        toSend=":1" + value + ";"
        ser.write(toSend.encode())
        gear=ac.getCarState(0,acsys.CS.Gear)
        gear = int(gear)
        gear = gear - 1
        if gear == 0:
            gear = "n"
        elif gear == -1:
            gear = "r"
        else:
            gear = str(gear)
        toSendGear = ":2" + gear + ";"
        ser.write(toSendGear.encode())
        if limitisset == 0:
            islimiteron=ac.getCarState(0,acsys.CS.IsEngineLimiterOn)
            islimiteron = int(islimiteron)
            if islimiteron == 1:
                toSendLimit = ":3" + value + ";"
                ser.write(toSendLimit.encode())
                limitisset=1
        count = 0
    else:
        count = count + 1
def acShutdown():
    global ser
    ac.log("called acShutdown()")
    ser.close()
