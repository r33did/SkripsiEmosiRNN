# com_serial.py is program to log data from arduino serial com
# import clean(data) to clean the raw data
# import write(data) to write data log to .csv format

# Created by Ahmad Akmal, 22-02-2021, for UGM EMG Research
import serial
import pandas as pd
import datetime as time
rawdata = []
pipi = []
alis = []
wkt = []
count = 0
header_list = ['Waktu','Pipi',"Alis"]
p = list(serial.tools.list_ports.comports())
arduino = serial.Serial(p[0].device,timeout=1,baudrate=9600)
arduino.flushInput()

while True:
    try:
        if count == 1000:
            rawdata.append(str(arduino.readline()))
            b = rawdata.decode('ISO-8859-1').strip()
            waktuReal = time.now()
            waktu = waktuReal.strftime('%H:%M:%S.%f')[:-3]
            c = b.split(',')
            pipi.append(c[0])
            alis.append(c[1])
            wkt.append(waktu)
            count+=1
            print(count)
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        break
    print("Logging Data Selesai")

# # def clean(L):
# #     newL = []
# #     for i in range(len(L)):
# #         temp = L[i][2:]
# #         newL.append(temp[:-5])
# #     return newL

# cleandata = clean(rawdata)

def write():
    d_t = list(zip(wkt,pipi,alis))
    df = pd.DataFrame(d_t, columns=header_list)
    nama_file = input("Masukkan nama file : ")
    df.to_csv('%s.csv'%nama_file,header=header_list,mode='w+')
    return df
write()

# ---------------------------EOL--------------------------
