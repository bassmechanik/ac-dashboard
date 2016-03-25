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

try:
    from sim_info import info
except:
    log_error()
    raise

ser = serial.Serial(port = 'COM3', baudrate = 10, timeout = 0)
count = 0
do_once = 1

def acMain(acVersion):
    global ac
    ac.log("called acMain()")
    return "Arduino Serial"
def acUpdate(deltaT):
    global do_once,ser,ac,acsys,count
    if do_once: # in der acMain ist noch kein Shared Memory gefüllt
        value =info.static.maxRpm
        value = str(round(value))
        toSend=":3" + value + ";"
        ser.write(toSend.encode())
        
        #toSend=":4" + "20" + ";" #Comment out to change drawsetpoint default 20% from maxRpm
        #ser.write(toSend.encode()) #Comment out to change drawsetpoint
    
        #toSend=":5" + "5" + ";"  #Comment out to change flashsetpoint default 5% from maxRpm
        #ser.write(toSend.encode()) #Comment out to change flashsetpoint
        do_once=0
        
    if count == 5:
        value=info.physics.rpms
        value = str(round(value))
        toSend=":1" + value + ";"
        ser.write(toSend.encode())
        gear=info.physics.gear
        gear = int(gear)
        gear = gear - 1
        if gear == 0:
            gear = "-"
        elif gear == -1:
            gear = "R"
        else:
            gear = str(gear)
        toSendGear = ":2" + gear + ";"
        ser.write(toSendGear.encode())
        count = 0
    else:
        count = count + 1
def acShutdown():
    global ser
    ac.log("called acShutdown()")
    ser.close()
