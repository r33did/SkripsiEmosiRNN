from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QSettings
import sys
import serial
import serial.tools.list_ports
import  time
import pyqtgraph as pg
import numpy as np
import pandas as pd
import datetime
import serial.tools.list_ports
import os
import sys
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import keras
from sklearn.metrics import confusion_matrix,classification_report

serial_port =  serial.Serial()
ptr = 0
class Serial_RX(QtCore.QThread):
    Serial_signal = pyqtSignal()
    Scope_signal = pyqtSignal()
    serial_display = ''
    serial_buffer = ''
    timer = time.process_time()
    def __init__(self,parent):
        QtCore.QThread.__init__(self)
        self.parent = parent
    def __del__(self):
        self.wait()
# =========RUN SCOPE=============
    def run(self):
        global ptr
        while True:
            if serial_port.is_open:

                if self.parent.Scope_Enable_chk.isChecked():
                    if self.parent.CSV_mode.isChecked():
                        error = False
                        try:
                            self.serial_buffer = serial_port.readline().decode("utf-8")
                            preprocess_str = self.serial_buffer
                            preprocess_str = preprocess_str.replace('\r','')
                            preprocess_str = preprocess_str.replace('\n', '')
                            separate_str = preprocess_str.split(',')
                            separate_val = [float(i) for i in separate_str]
                            #print(separate_val)
                            self.serial_display = self.serial_buffer
                            self.parent.x_plt_arr = np.append(self.parent.x_plt_arr, ptr)
                            self.parent.y_plt_arr = np.append(self.parent.y_plt_arr, separate_val[0])
                            self.parent.y_plt_arr2 = np.append(self.parent.y_plt_arr2, separate_val[1])
                            ptr+=1

                        except:
                            print('Read CSV Error')
                            error = True
                        if not error:
                            self.Serial_signal.emit()
                            self.Scope_signal.emit()
                    elif self.parent.Protocol_mode.isChecked():
                        pass
                else:
                    error = False
                    data_to_update = False
                    try:
                        if serial_port.inWaiting()>0:

                            #print(delta_time)
                            bytesToRead = serial_port.inWaiting()
                            data = serial_port.read(bytesToRead)
                            self.serial_buffer = ''

                            #if self.mode == 'ASCII':
                            if self.parent.ASCII_mode.isChecked():
                                self.serial_buffer += data.decode("utf-8")

                            #elif(self.mode == 'HEX'):
                            elif  self.parent.HEX_mode.isChecked():
                                delta_time = (time.clock() - self.timer)
                                self.timer = time.clock()
                                if delta_time> 0.025:
                                    self.serial_buffer += '\r\n'
                                for b in data:
                                    self.serial_buffer +=  ' '+format(b, '02x')+' '
                            self.serial_display = self.serial_buffer
                            data_to_update = True

                    except:
                        print('read error')
                        error = True
                    if not error and data_to_update:
                        self.Serial_signal.emit()


class Serial_TX(QtCore.QThread):
    data_to_send = ''
    def __init__(self,data_to_send):
        QtCore.QThread.__init__(self)
        self.data_to_send = data_to_send
    def __del__(self):
        self.wait()
    def run(self):
        try:
            serial_port.write(self.data_to_send.encode())
        except:
            print('send error')
class main_widget(QWidget):
    x_plt_arr =  np.array([])
    y_plt_arr = np.array([])
    y_plt_arr2 = np.array([])
    def __init__(self, parent,settings):
        self.settings = settings
        super().__init__(parent)
        self.setupUI()
        self.settup_scope()
    def settup_scope(self):
        self.GL = pg.GraphicsLayoutWidget()
        self.scope_win = QMainWindow()
        self.scope_win.resize(1000, 600)
        self.scope_win.setWindowTitle('pyqtgraph example')
        self.scope_win.setCentralWidget(self.GL)
        self.plt = self.GL.addPlot(title="Updating plot")
        self.plt.showGrid(x=True, y=True, alpha=0.3)
        self.curve = self.plt.plot(pen='y')
        self.curve2 = self.plt.plot(pen='b')
    def show_scope(self):
        if not self.scope_win.isVisible():
            self.scope_win.show()
# !!!!!!!!!!!!!!!!!!!!!INI SCOPE UPDATE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def scope_update(self):
        plot_size = 1000
        if serial_port.is_open:
            try:
                x_data = self.x_plt_arr[max(0, len(self.x_plt_arr) - plot_size):len(self.x_plt_arr) - 1:]
                y_data = self.y_plt_arr[max(0, len(self.y_plt_arr) - plot_size):len(self.y_plt_arr) - 1:]
                y_data2 = self.y_plt_arr2[max(0, len(self.y_plt_arr2) - plot_size):len(self.y_plt_arr2) - 1:]

                self.plt.enableAutoRange(x=True, y=True)
                self.plt.setMouseEnabled(x=False, y=False)
                self.curve.setData(x_data, y_data)
                self.curve2.setData(x_data,y_data2)
            except:
                print('plot error')

    def scope_show_all_data(self):
        self.curve.setData(self.x_plt_arr, self.y_plt_arr)
        self.curve2.setData(self.x_plt_arr, self.y_plt_arr2)
        self.plt.enableAutoRange(x=True, y=True)
        self.plt.setMouseEnabled(x=True, y=True)
        QtGui.QApplication.processEvents()
        print('scope_show_all_data')
    def get_port_list(self):
        port_list = []
        for i in serial.tools.list_ports.comports(include_links=False):
            port_list.append(i.device)
        return port_list
    def update_port_list(self):
        print('update_port_list')
        self.Port_select.clear()
        self.Port_select.addItems(self.get_port_list())
        self.Port_select.update()
    def serial_connect(self):

        serial_port.port = str(self.Port_select.currentText())

        serial_port.baudrate = int(self.Buad_select.currentText())
        print(serial_port)
        try:
            serial_port.open()
        except:
            print('Serial error')
            self.serial_error_dialog()
            return
        self.connection_update()
        print('Connected')
        self.serial_log_clear()
        self.settings.setValue('last_connect_port', serial_port.port)
        self.settings.setValue('last_connect_baud', str(serial_port.baudrate))
        if self.Scope_Enable_chk.isChecked():
            self.show_scope()
    def serial_disconnect(self):
        serial_port.close()
        self.connection_update()
        print('Disconnected')
        if self.Scope_Enable_chk.isChecked():
            self.scope_show_all_data()
    def serial_log_update(self):
        self.Serial_log.insertPlainText(self.Serial_RX_Thread.serial_display)
        self.Serial_log.verticalScrollBar().setValue(self.Serial_log.verticalScrollBar().maximum())
# ==================UPDATE CLEAR SERIAL DAN CONNECTION========================
    def serial_log_clear(self):
        global ptr
        self.Serial_log.setPlainText('')
        self.x_plt_arr = np.array([])
        self.y_plt_arr = np.array([])
        self.y_plt_arr2 = np.array([])
        ptr = 0
    def connection_update(self):
        Serial_Open = serial_port.is_open
        self.send_button.setEnabled(Serial_Open)
        self.disconnect_button.setEnabled(Serial_Open)
        self.connect_button.setEnabled(not Serial_Open)
        self.Port_select.setEnabled(not Serial_Open)
        self.port_refresh_button.setEnabled(not Serial_Open)
        self.Buad_select.setEnabled(not Serial_Open)
        self.ASCII_mode.setEnabled(not Serial_Open)
        self.HEX_mode.setEnabled(not Serial_Open)
        self.Scope_Enable_chk.setEnabled(not Serial_Open)
        self.CSV_mode.setEnabled(not Serial_Open)
        self.Protocol_mode.setEnabled(not Serial_Open)
# ===================KIRIM SERIAL KE THREAD=====================
    def serial_send(self):
        data_to_send = self.text_for_send.text()
        if self.CR.isChecked():
            data_to_send += '\r'
        if self.NL.isChecked():
            data_to_send += '\n'
        self.Serial_TX_Thread = Serial_TX(data_to_send)
        self.Serial_TX_Thread.start()
        print('send : ' + data_to_send)

        self.text_for_send.setText('')
    def serial_error_dialog(self):
        serial_error_msg = QMessageBox()
        serial_error_msg.setIcon(QMessageBox.Warning)
        serial_error_msg.setText("Error openning serial port "+serial_port.port)
        #serial_error_msg.setInformativeText("This is additional information")
        serial_error_msg.setWindowTitle("Warning message")

        serial_error_msg.setStandardButtons(QMessageBox.Ok )
        serial_error_msg.exec_()
# ====================SERIAL SETTING======================
    def serial_setting_groupBox(self):
        serial_setting = QGroupBox('Serial port setting')
        Hlayout = QHBoxLayout(self)
        l1 = QLabel()
        l1.setText('Port')
        l2 = QLabel()
        l2.setText('Baud rate')
        self.port_refresh_button = QPushButton('Refresh', self)
        self.port_refresh_button.clicked.connect(self.update_port_list)

        self.connect_button = QPushButton('Connect', self)
        self.connect_button.clicked.connect(self.serial_connect)
        self.disconnect_button = QPushButton('Disconnect', self)
        # self.disconnect_button.setEnabled(False)
        self.disconnect_button.clicked.connect(self.serial_disconnect)

        self.Port_select = QComboBox()
        port_list = self.get_port_list()
        self.Port_select.addItems(port_list)

        last_connect_port = self.settings.value('last_connect_port', type=str)
        if last_connect_port in port_list:
            self.Port_select.setCurrentIndex(port_list.index(last_connect_port))

        self.Buad_select = QComboBox()
        baud_list = ['300', '600', '1200', '2400', '4800', '9600', '14400', '19200', '28800', '38400', '57600', '115200']
        self.Buad_select.addItems(baud_list)
        last_connect_baud = self.settings.value('last_connect_baud', type=str)
        if last_connect_baud in baud_list:
            self.Buad_select.setCurrentIndex(baud_list.index(last_connect_baud))


        H_Spacer1 = QSpacerItem(150, 10, QSizePolicy.Expanding)
        Hlayout.addWidget(l1)
        Hlayout.addWidget(self.Port_select)
        Hlayout.addWidget(self.port_refresh_button)
        Hlayout.addWidget(l2)
        Hlayout.addWidget(self.Buad_select)
        Hlayout.addWidget(self.connect_button)
        Hlayout.addWidget(self.disconnect_button)
        Hlayout.addItem(H_Spacer1)
        # Vlayout.addLayout(Hlayout_0)
        serial_setting.setLayout(Hlayout)
        return serial_setting
# ===================SCOPE ENABLE================================
    def Scope_Enable_update(self):
        if self.Scope_Enable_chk.isChecked():
            self.Display_settings_Taps_Widget.setTabEnabled(1,True)
        else:
            self.Display_settings_Taps_Widget.setTabEnabled(1, False)
# ====================SETTING TAB================================
    def Display_settings_Taps(self):
        self.Display_settings_Taps_Widget = QTabWidget()
        Log_settings_tab = QWidget()
        Scope_settings_tab = QWidget()
        self.Display_settings_Taps_Widget.addTab(Log_settings_tab, "Log Settings")
        self.Display_settings_Taps_Widget.addTab(Scope_settings_tab, "Scope Settings")
        ############################################################################
        Log_Settings_Hlayout = QHBoxLayout(self)
        Display_Mode_Label = QLabel()
        Display_Mode_Label.setText('Display Mode')
        self.ASCII_mode = QRadioButton("ASCII")
        self.ASCII_mode.setChecked(True)
        self.HEX_mode = QRadioButton("HEX")
        clear_log_button = QPushButton('Clear', self)
        clear_log_button.clicked.connect(self.serial_log_clear)
        self.Scope_Enable_chk = QCheckBox("Scope Enable")
        self.Scope_Enable_chk.clicked.connect(self.Scope_Enable_update)
        H_Spacer = QSpacerItem(10, 10, QSizePolicy.Expanding)
        mini_H_Spacer = QSpacerItem(50, 10)
        Log_Settings_Hlayout.addWidget(Display_Mode_Label)
        Log_Settings_Hlayout.addWidget(self.ASCII_mode)
        Log_Settings_Hlayout.addWidget(self.HEX_mode)
        Log_Settings_Hlayout.addWidget(clear_log_button)
        Log_Settings_Hlayout.addItem(mini_H_Spacer)
        Log_Settings_Hlayout.addWidget(self.Scope_Enable_chk)
        Log_Settings_Hlayout.addItem(H_Spacer)
        Log_settings_tab.setLayout(Log_Settings_Hlayout)
        ############################################################################
        Scope_Settings_Hlayout = QHBoxLayout(self)
        Data_Format_Label = QLabel()
        Data_Format_Label.setText('Data Format')
        self.CSV_mode = QRadioButton("CSV")
        self.CSV_mode.setChecked(True)
        self.Protocol_mode = QRadioButton("Protocol")
        open_scope_button = QPushButton('Open Scope', self)
        open_scope_button.clicked.connect(self.show_scope)
        H_Spacer2 = QSpacerItem(10, 10, QSizePolicy.Expanding)
        Scope_Settings_Hlayout.addWidget(Data_Format_Label)
        Scope_Settings_Hlayout.addWidget(self.CSV_mode)
        Scope_Settings_Hlayout.addWidget(self.Protocol_mode)
        Scope_Settings_Hlayout.addWidget(open_scope_button)
        Scope_Settings_Hlayout.addItem(H_Spacer2)
        Scope_settings_tab.setLayout(Scope_Settings_Hlayout)
        ############################################################################
        self.Display_settings_Taps_Widget.setFixedHeight(75)

        return self.Display_settings_Taps_Widget
    def Sending_console(self):
        Vlayout = QVBoxLayout(self)
        Hlayout_1 = QHBoxLayout(self)
        self.text_for_send = QLineEdit()
        self.send_button = QPushButton('Send', self)
        self.send_button.clicked.connect(self.serial_send)
        Hlayout_1.addWidget(self.text_for_send)
        Hlayout_1.addWidget(self.send_button)
        Vlayout.addLayout(Hlayout_1)

        ################################
        Hlayout_2 = QHBoxLayout(self)
        l3 = QLabel()
        l3.setText('Line ending')
        self.CR = QCheckBox("<CR>")
        self.NL = QCheckBox("<NL>")
        H_Spacer2 = QSpacerItem(150, 10, QSizePolicy.Expanding)

        Hlayout_2.addWidget(l3)
        Hlayout_2.addWidget(self.CR)
        Hlayout_2.addWidget(self.NL)
        Hlayout_2.addItem(H_Spacer2)
        Vlayout.addLayout(Hlayout_2)
        Sending_console_widget = QWidget()
        Sending_console_widget.setLayout(Vlayout)
        return Sending_console_widget
    def setupUI(self):

        main_Vlayout = QVBoxLayout(self)
        ################################

        main_Vlayout.addWidget(self.serial_setting_groupBox())

        ################################
        main_Vlayout.addWidget(self.Display_settings_Taps())

        self.Serial_log = QPlainTextEdit()

        self.Serial_log.setReadOnly(True)

        main_Vlayout.addWidget(self.Serial_log)

        ################################

        main_Vlayout.addWidget(self.Sending_console())

        ################################
        self.connection_update()
        self.setLayout(main_Vlayout)
        self.Scope_Enable_update()

        self.Serial_RX_Thread = Serial_RX(self)
        self.Serial_RX_Thread.start()
        self.Serial_RX_Thread.Serial_signal.connect(self.serial_log_update)
        self.Serial_RX_Thread.Scope_signal.connect(self.scope_update)

class main_window(QMainWindow):
    def __init__(self,settings ):
        self.settings = settings
        super(QMainWindow, self).__init__()
        #QMainWindow.__init__(self)
        self.initUI()
    def initUI(self):
        self.setGeometry(300, 300, 500, 600)
        self.setWindowTitle("Serial Monitor")
        self.setWindowIcon(QtGui.QIcon('py_logo.png'))
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        impMenu = QMenu('Import', self)
        imp_txt_Act = QAction('Import text file', self)
        imp_csv_Act = QAction('Import CSV file', self)
        imp_byte_Act = QAction('Import Protocol file', self)
        impMenu.addAction(imp_txt_Act)
        impMenu.addAction(imp_csv_Act)
        impMenu.addAction(imp_byte_Act)

        expMenu = QMenu('Export', self)
        exp_txt_Act = QAction('Export text file', self)
        exp_csv_Act = QAction('Export CSV file', self)
        exp_byte_Act = QAction('Export Protocol file', self)
        expMenu.addAction(exp_txt_Act)
        expMenu.addAction(exp_csv_Act)
        expMenu.addAction(exp_byte_Act)

        fileMenu.addMenu(impMenu)
        fileMenu.addMenu(expMenu)

        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
        toolsMenu = mainMenu.addMenu('Tools')
        helpMenu = mainMenu.addMenu('Help')
        self.main_widget = main_widget(self,self.settings)
        self.setCentralWidget( self.main_widget)




    def closeEvent(self, event):

        if serial_port.is_open:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("Are you sure you want to quit?")
            msg.setInformativeText("Serial port still connected.")
            msg.setWindowTitle("MessageBox demo")
            msg.setWindowTitle("Warning message")

            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)


            retval = msg.exec_()
            if retval == QMessageBox.Ok:
                print('Exit conform')
                app = QtGui.QApplication.instance()
                app.closeAllWindows()
            else:
                event.ignore()

        else:
            app = QtGui.QApplication.instance()
            app.closeAllWindows()

def main():
    app = QApplication(sys.argv)
    settings = QSettings('Meng\'s Lab', 'Serial Monitor')
    w = main_window(settings)
    w.show()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()
