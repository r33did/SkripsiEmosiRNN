# akuisisi_data.py

import serial
import pandas as pd
from datetime import datetime
import serial.tools.list_ports as listPorts

waktuReal = []
emgFrontalis = []
emgCorrugator = []

p = list(listPorts.comports())
    # baca serial arduino, serial.Serial(port,baudrate)
# arduino = serial.Serial() -> isi portnya nanti sesuai colok dimana

# function to read arduino from PC with USB connection
def baca():
    arduinoData = arduino.readline()
    # Encode UTF 8 to ASCII format ISO-8859-1
    dataUTF8 = arduinoData.decode("ISO-8859-1").strip()
    data = dataUTF8.split(',')
    dataFrontalis = int(data[0])/1023*5
    dataCorrugator = int(data[1])/1023*5
    emgFrontalis.append(dataFrontalis)
    emgCorrugator.append(dataCorrugator)
    # strftime(): %Y = year, %m = month, %d = day, ///
    # %H:%M:%S = hour:minute:second
    realTime = datetime.now()
    realTimestr = realTime.strftime("%H:%M:%S.%f")
    waktuReal.append(realTimestr)
    return waktuReal, emgFrontalis, emgCorrugator

def archive():
    d_t = list(zip(waktuReal,emgFrontalis,emgCorrugator))
    dataFrame = pd.DataFrame(d_t, columns=['Waktu','Pipi','Alis'])
    nama_file = input('Insert file name: ')
    dataFrame.to_csv('%s.csv'%nama_file)
    return dataFrame

    try:
        while(True):
            baca()
    except KeyboardInterrupt:
        arduino.close()
        print("Arduino has disconnected")
        archive()