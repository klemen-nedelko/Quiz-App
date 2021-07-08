import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
#functions import
from functions import frame1, frame2, frame3, frame4, grid

#initiallize GUI application
app = QApplication(sys.argv)
#window and settings
window = QWidget()
window.setWindowTitle("QUIZ GAME")
window.setFixedWidth(1000)
window.setFixedHeight(720)
window.setWindowIcon(QtGui.QIcon('logo.png'))
#place window in (x,y) coordinates
window.setStyleSheet("background: #1D1A1A;")
#klicanje zacetnega menija
frame1()

window.setLayout(grid)

#prikaz window
window.show()
sys.exit(app.exec()) 
#terminate the app