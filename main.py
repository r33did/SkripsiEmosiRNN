import serial
import pandas as pd
import datetime
import serial.tools.list_ports
import os
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
header_list = ['Waktu','Pipi','Alis']
akuisisi()
write()
filtering()
#extract_feature('Data_filter')
