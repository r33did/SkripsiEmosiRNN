from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
class myWindow(QMainWindow):
    def __init__(self):
        super(myWindow,self).__init__()
        self.initUI()
        self.setGeometry(0, 0, 1366, 768)
        self.setWindowTitle('Real Time EMG Identificaiton Emotion')

    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText('Real Time EMG')
        self.label.move(670,20)

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText('Save')
        self.b1.clicked.connect(self.tersimpan)

    def tersimpan(self):
        self.label.setText('Data telah tersimpan')
        self.update()

    def update(self):
        self.label.adjustSize()

def window():
    app = QApplication(sys.argv)
    win = myWindow()
    win.show()
    sys.exit(app.exec_())

window()