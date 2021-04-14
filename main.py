import serial
import pandas as pd
import datetime
import serial.tools.list_ports
import os
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
from com_serial import *
from filter import *
from model import *

rawdata = []
pipi = []
alis = []
wkt = []
count = 0
header_list = ['Waktu','Pipi']
p = list(serial.tools.list_ports.comports())
arduino = serial.Serial(p[0].device,timeout=1,baudrate=74880)
arduino.flushInput()

rawdata = []
pipi = []
alis = []
wkt = []
count = 0
header_list = ['Waktu','Pipi']
data1n = []
data2n = []
root = 'Filtered'
emosi = ['kaget','marah','santai','senang']
p = list(serial.tools.list_ports.comports())
arduino = serial.Serial(p[0].device,timeout=1,baudrate=74880)
arduino.flushInput()

data1n = []
data2n = []
root = 'Filtered'
emosi = ['kaget','marah','santai','senang']

akuisisi_data()
write()
filtering()
extract_feature('Data_filter')
