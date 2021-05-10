# com_serial.py is program to log data from arduino serial com
# import clean(data) to clean the raw data
# import write(data) to write data log to .csv format

# Created by Ahmad Akmal, 22-02-2021, for UGM EMG Research
import serial
import pandas as pd
import datetime
import serial.tools.list_ports
import os
rawdata = []
pipi = []
alis = []
wkt = []
count = 0
d = 0
e = 0
header_list = ['Waktu','Pipi','Alis']
def akuisisi():
    p = list(serial.tools.list_ports.comports())
    arduino = serial.Serial(p[0].device,baudrate=115200)
    arduino.flushInput()
    if not arduino.isOpen():
        arduino.open()
    global count
    while True:
        try:
            if count <= 1000:
                data = arduino.readline()
                b = data.decode("ISO-8859-1").strip()
                waktuReal = datetime.datetime.now()
                waktu = waktuReal.strftime('%H:%M:%S.%f')[:-3]
                c = b.split(',')
                d = (int(c[0])/1024)*5
                e = (int(c[1])/1024)*5
                pipi.append(c[0])
                alis.append(c[1])
                wkt.append(waktu)
                count+=1
                print(b)
                if count == 1000:
                    arduino.close()
                    print("Logging Data Selesai")
                    break
        except KeyboardInterrupt:
            print("Keyboard Interrupt")
            arduino.close()
            break

def write():
    root = 'Data_raw'
    d_t = list(zip(wkt,pipi,alis))
    df = pd.DataFrame(d_t, columns=header_list)
    nama_file = input("Masukkan nama file : ")
    finaldirs = os.path.join(root,'%s.csv'%nama_file)
    df.to_csv(finaldirs,header=header_list,mode='w+')
    print("Logging data selesai !")
    return df
akuisisi()
write()
# ---------------------------EOL--------------------------
