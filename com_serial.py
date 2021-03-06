# com_serial.py is program to log data from arduino serial com
# import clean(data) to clean the raw data
# import write(data) to write data log to .csv format

# Created by Ahmad Akmal, 22-02-2021, for UGM EMG Research
import serial
import pandas as pd
rawdata = []
count = 0
header_list = ['pipi']
arduino = serial.Serial("COM6",timeout=1,baudrate=9600)
arduino.flushInput()

while True:
    try:
        rawdata.append(str(arduino.readline()))
        count+=1
        print(count)
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        break
print("Logging Data Selesai")

def clean(L):
    newL = []
    for i in range(len(L)):
        temp = L[i][2:]
        newL.append(temp[:-5])
    return newL

cleandata = clean(rawdata)

def write(L):
    df = pd.DataFrame(L)
    nama_file = input("Masukkan nama file : ")
    df.to_csv('%s.csv'%nama_file,header=header_list,mode='w+')
    return df
write(cleandata)

# ---------------------------EOL--------------------------
