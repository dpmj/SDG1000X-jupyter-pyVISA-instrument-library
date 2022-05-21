import visa
from visa import constants
import vxi11
import csv
import pandas as pd
import time
import math
import os
import numpy as np

# GPIB INIT
# visa.log_to_screen()
SG =  vxi11.Instrument("192.168.1.119")
OSC = visa.ResourceManager('@py').get_instrument('TCPIP0::192.168.1.121::inst0::INSTR')
OSC.timeout=2500000

# IDENTIFYING
print("SG found: " + SG.ask("*IDN?").strip())
print("OSC found: " + OSC.query('*IDN?').strip())

#OSC Setting-up

OSC.write(':CHANnel1:DISPlay ON')
OSC.write(':DISPlay:SIDebar MEASurements')
OSC.write(':MEASure:VPP CHANnel1')

#SG Setting-up

SG.ask("CH1:VOLT 12")
SG.ask("CH2:VOLT 20")

SG.ask("CH1:CURRent 0.3")
SG.ask("CH2:CURRent 3.2")

SG.ask("OUTPut CH1,ON")
SG.ask("OUTPut CH2,ON")

volt_Sweep=np.arange(20,32.5,0.5)
current_Sweep=[]
measured_Osc=[]

#Allow time for the measurement to stabilize at the final values

for V in volt_Sweep:

  SG.ask("CH2:VOLT %f" %V)

  if V==31 or V==31.5 or V==32:

    time.sleep(60)

  else:

    time.sleep(1)

  current_Sweep.append(SG.ask("MEASure:CURRent? CH2"))
  measured_Osc.append(OSC.query(':MEASure:VRMS? CHANnel1'))


voltage_Data=pd.DataFrame(volt_Sweep)
current_Data=pd.DataFrame(current_Sweep)
measured_Voltage_Data=pd.DataFrame(measured_Osc)

pd.concat([voltage_Data,current_Data,measured_Voltage_Data],axis=1).to_csv("data5.csv")

print("Data written to CSV")

SG.ask("OUTPut CH1,OFF")
SG.ask("OUTPut CH2,OFF")
