from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys




class View(QtWidgets.QMainWindow):



    def __init__(self):
        super(View, self).__init__()
        uic.loadUi('untitled.ui', self)


        self.show()


    def main(self):
        print('In main of view')

app = QtWidgets.QApplication(sys.argv)
window = View()
app.exec_()