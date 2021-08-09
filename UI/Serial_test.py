import serial
import serial.tools.list_ports
import threading
import time
serial_port = serial.Serial()
def rx_thread_fc():
    while True:
        #print('recieve')
        #time.sleep(1)
        if serial_port.is_open:
            if serial_port.inWaiting() > 0:
                data = serial_port.read(serial_port.inWaiting())
                print(data)
def get_port_list():
    port_list = []
    for i in serial.tools.list_ports.comports(include_links=False):
        port_list.append(i.device)
    return port_list

while True:
    connect_err_flag = False
    print("Select port");
    port_list = get_port_list()
    for port_i in range(len(port_list)):
        print('[',port_i,']',port_list[port_i])
    while True:
        input_err_flag = False
        try:
            port_select = int(input())
        except:
            print("invalid number")
            input_err_flag = True
        if not input_err_flag:
            break
    serial_port.baudrate = 115200
    serial_port.port = port_list[port_select]

    try:
        serial_port.open()
    except:
        print('Serial error')
        connect_err_flag = True
    if not connect_err_flag:
        break
print("Serial connection establish")

rx_thread = threading.Thread(target=rx_thread_fc)
rx_thread.start()
while True:
    data_to_send = input()
    data_to_send += '\n'
    serial_port.write(data_to_send.encode())
