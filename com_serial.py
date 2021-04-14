# com_serial.py is program to log data from arduino serial com
# import clean(data) to clean the raw data
# import write(data) to write data log to .csv format

# Created by Ahmad Akmal, 22-02-2021, for UGM EMG Research

def akuisisi_data():
    while True:
        try:
            if count <= 1000:
                data = arduino.readline()
                b = data.decode("ISO-8859-1").strip()
                waktuReal = datetime.datetime.now()
                waktu = waktuReal.strftime('%H:%M:%S.%f')[:-3]
                c = b.split(',')
                pipi.append(c[0])
                alis.append(c[1])
                wkt.append(waktu)
                count+=1
                print(b)
                if count == 1000:
                    arduino.close()
                    break
        except KeyboardInterrupt:
            print("Keyboard Interrupt")
            arduino.close()
            break
    print("Logging Data Selesai")

def write():
    root = 'Data_raw'
    d_t = list(zip(wkt,pipi,alis))
    df = pd.DataFrame(d_t, columns=header_list)
    nama_file = input("Masukkan nama file : ")
    finaldirs = os.path.join(root,'%s.csv'%nama_file)
    df.to_csv(finaldirs,header=header_list,mode='w+')
    print("Logging data selesai !")
    return df

# ---------------------------EOL--------------------------
