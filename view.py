from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage
from PyQt5 import uic, QtWidgets
import sys
from model import VideoFrameCapture

class Controller:
    def __init__(self):
        self.camSDK, self.cam = self.openCamera()



        self.view = View()
        #self.view.closeCamButton.clicked.connect(VideoFrameCapture.discon(self.cam, self.camSDK))
        #self.main()

        #self.closeCamera(self.cam, self.camSDK)

    # def main(self):
    #     print("Main of controller")
    #     self.view.totalDis.setText("INFINITY")

    def openCamera(self):
        camSDK = VideoFrameCapture.getcamSDK()
        cam = VideoFrameCapture.getcam(camSDK)
        return camSDK, cam

    def closeCamera(self, cam, camsdk):
        VideoFrameCapture.discon(cam, camsdk)


# class Image(QThread):
#     ImageUpdate = pyqtSignal(QImage)
#     def run(self):
#         self.ThreadActive = True
#         while self.ThreadActive:
#             image = VideoFrameCapture()

class View(QtWidgets.QMainWindow):

    def __init__(self):
        super(View, self).__init__()
        uic.loadUi('untitled.ui', self)
        self.totalDis.setText("INFINITY")
        self.xDis.setText("INFINITY")
        self.yDis.setText("INFINITY")
        self.fwhm.setText("INFINITY")
        self.spotSize.setText("INFINITY")
        self.d4sigma.setText("INFINITY")
        self.circularity.setText("INFINITY")
        self.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Controller()
    app.exec_()