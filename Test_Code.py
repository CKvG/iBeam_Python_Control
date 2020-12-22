# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 17:53:37 2020

@author: grundch
"""


import Laser_DLL as iBeam
import time


PORT = 'COM3'

ser = iBeam.connect(PORT)

iBeam.getChannelInfo(ser) #getTerminalString

iBeam.getLaserTemp(ser) #getTerminal

iBeam.getLaserPowerIn_uW(ser)

iBeam.setLaserPowerIn_uW(ser, 1 , 10)

iBeam.getLaserPowerIn_uW(ser)

#iBeam.setLaserON(ser)

iBeam.getLaserStatus(ser)

time.sleep(2)

#iBeam.setLaserOFF(ser)

iBeam.disconnect(ser)
