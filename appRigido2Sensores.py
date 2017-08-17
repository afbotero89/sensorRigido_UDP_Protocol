# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rigidoBotonesConexion.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.axes_grid1 import make_axes_locatable, axes_size
import socket
import sys
import binascii
import threading
import numpy as np
import socket
import scipy.ndimage
import sys, struct
from pylab import *
import time
import sqlite3
import ast
import time
import recvPlataforma1
ion()

maxint = 2 ** (struct.Struct('i').size * 8 - 1) - 1
sys.setrecursionlimit(maxint)

class Ui_MainWindow(object):
    def __init__(self):
        print("init")
        self.fig = plt.figure(facecolor='#222222',figsize=(18,9))
        self.fig.set_size_inches(18,9)
        ax = plt.Axes(self.fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        self.fig.add_axes(ax)
        self.fig.canvas.draw()
        #self.fig.canvas.toolbar.pack_forget()
        #plt.show(block=False)
        self.vectorDatosDistribucionPresion = []
        self.vectorDesencriptado = []
        self.iniciaTramaDeDatos = False
        self.columnas = 48;
        self.filas = 48;
        axis = plt.gca()
        axis.get_xaxis().set_visible(False)
        axis.get_yaxis().set_visible(False)
        matriz = [[0 for x in range(self.columnas)] for x in range(self.filas)] 
        matriz[0][0] = 255
        matrizSensor2 = [[0 for x in range(self.columnas)] for x in range(self.filas)] 
        #matrizSensor2[0][0] = 255
        matrizCompleta = np.concatenate((matriz,matrizSensor2),axis=1)
        matrizCompleta[0][0] = 255
        plt.set_cmap('jet')

        self.cbar = self.fig.colorbar(plt.imshow(matrizCompleta), ticks=[5,125,250], fraction=0.024, pad=0.05)
        self.cbar.ax.set_yticklabels(['Baja','Medio','Alto'])
        #divider = make_axes_locatable(plt.gca())
        #cax = divider.append_axes("right","5%",pad="3%")
        #plt.colorbar(plt.imshow(matrizCompleta),cax=cax)
        
        self.initData = scipy.ndimage.zoom(matrizCompleta, 3)
        #self.contour = plt.contour(data)
        
        self.imagen = plt.imshow(self.initData, interpolation = 'nearest')
        self.contador = 0
        self.contour_axis = plt.gca()
        self.sensor1Conectado = False
        self.sensor2Conectado = False
        self.defaultNumberOfPlatforms = 2
        self.numberOfPlatforms = 2
        self.intensityAdjustment = 250

        self.sensor1Conectado = False
        
        # Sensor 1 configuracion plataforma clara
        self.UDP_IP1 = "192.168.0.124"
        self.UDP_PORT1 = 10001

        self.UDP_IP_CLIENT1 = "192.168.0.101"
        self.UDP_PORT_CLIENT1 = 2233

        self.idSensor1 = "1"

        # Sensor 2 configuracion plataforma oscura
        self.UDP_IP2 = "192.168.0.124"
        self.UDP_PORT2 = 10000

        self.UDP_IP_CLIENT2 = "192.168.0.107"
        self.UDP_PORT_CLIENT2 = 2233

        self.idSensor2 = "2"

        self.visualizarPresion = False

        self.green_red_Button_Sensor1 = False

        self.green_red_Button_Sensor2 = False
        #plt.gca().invert_yaxis()
            
    def sqlDataBase(self):
        
        self.conn = sqlite3.connect('distribucionPresionSensorRigido.db', check_same_thread=False, timeout=10)
        self.c = self.conn.cursor()
        
    def setupUi(self, MainWindow):
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1522, 953)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1520, 853))
        MainWindow.setMaximumSize(QtCore.QSize(1522, 853))
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.graphicsView_2 = QtWidgets.QGraphicsView(self.centralWidget)
        self.graphicsView_2.setGeometry(QtCore.QRect(-20, 0, 2041, 91))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView_2.sizePolicy().hasHeightForWidth())
        self.graphicsView_2.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        self.graphicsView_2.setPalette(palette)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.graphicsView_2.setBackgroundBrush(brush)
        self.graphicsView_2.setObjectName("graphicsView_2")

        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(1160, 18, 270, 61))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("img/logoGIBIC.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        self.titleLabel = QtWidgets.QLabel(self.centralWidget)
        self.titleLabel.setGeometry(QtCore.QRect(675, 10, 311, 71))
        self.titleLabel.setText("Plantar pressure")
        self.titleLabel.setStyleSheet("background-color: black; color:white; font size: 28pt; font-size: 22pt;")
        self.titleLabel.setScaledContents(True)
        self.titleLabel.setObjectName("titleLabel")

        self.gridLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 100, 1451, 751))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        
        canvas = FigureCanvas(self.fig)
        self.gridLayout.addWidget(canvas)
            
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")

        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setText("Connecting...")
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok) 

        self.msg1 = QtWidgets.QMessageBox()
        self.msg1.setIcon(QtWidgets.QMessageBox.Information)
        self.msg1.setText("Sensor desconectado")
        self.msg1.setStandardButtons(QtWidgets.QMessageBox.Ok) 

        # Push button
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setStyleSheet("background-color: red; border-style: outset; border-width: 1px; border-radius: 10px; border-color: beige; padding: 6px;")
        self.pushButton.setGeometry(QtCore.QRect(160, 35, 20, 20))
        self.pushButton.setObjectName("pushButton")

        self.connectedSensor = QtWidgets.QPushButton(self.centralWidget)
        self.connectedSensor.setStyleSheet("background-color: red; color: white; border-radius: 10px;")
        self.connectedSensor.setGeometry(QtCore.QRect(10, 30, 140, 32))
        self.connectedSensor.setObjectName("connectedSensor")

        self.pushButton_1 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_1.setStyleSheet("background-color: red; border-style: outset; border-width: 1px; border-radius: 10px; border-color: beige; padding: 6px;")
        self.pushButton_1.setGeometry(QtCore.QRect(360, 35, 20, 20))
        self.pushButton_1.setObjectName("pushButton1")

        self.connectedSensor_1 = QtWidgets.QPushButton(self.centralWidget)
        self.connectedSensor_1.setStyleSheet("background-color: red; color: white; border-radius: 10px;")
        self.connectedSensor_1.setGeometry(QtCore.QRect(210, 30, 140, 32))
        self.connectedSensor_1.setObjectName("connectedSensor")

        self.spinBox = QtWidgets.QSpinBox(self.centralWidget)
        self.spinBox.setGeometry(QtCore.QRect(175, 93, 48, 31))
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(2)
        self.spinBox.setValue(2)
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setStyleSheet("border-radius: 2px;")

        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(35, 100, 151, 16))
        self.label_2.setObjectName("label_2")
        self.label_2.setStyleSheet("color:white;")

        self.label_DivisionSensor = QtWidgets.QLabel(self.centralWidget)
        self.label_DivisionSensor.setGeometry(QtCore.QRect(700, 143, 2, 665))
        self.label_DivisionSensor.setStyleSheet("background-color: black;")

        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GIBIC group"))
        self.pushButton.setText(_translate("MainWindow", ""))
        self.connectedSensor.clicked.connect(self.conectarSensor1)
        self.connectedSensor_1.clicked.connect(self.conectarSensor2)
        
        self.connectedSensor.setText(_translate("MainWindow", "Connect 1"))
        self.connectedSensor_1.setText(_translate("MainWindow", "Connect 2"))

        self.label_2.setText(_translate("MainWindow", "Number of platforms:"))
        self.spinBox.valueChanged.connect(self.valueChangedSpinBox)
        #self.groupRadioButton.buttonClicked[int].connect(self.ButtonGroupClicked)

    #def ButtonGroupClicked(self,clicked):
        #print("radio button clicked",clicked*(-1))

    def valueChangedSpinBox(self):

        self.numberOfPlatforms = self.spinBox.value()
        if self.numberOfPlatforms == 1:

            #self.radioButton.setVisible(True)
            #self.radioButton_1.setVisible(False)
            #self.radioButton_2.setVisible(False)

            self.pushButton.setVisible(True)
            self.pushButton_1.setVisible(False)
 #           self.pushButton_3.setVisible(False)

            self.pushButton.setStyleSheet("background-color: red; border-radius: 10px;")
            self.pushButton_1.setStyleSheet("background-color: green; border-radius: 10px;")

            matriz = [[0 for x in range(self.columnas)] for x in range(self.filas)] 
            matriz[0][0] = 255
            data = scipy.ndimage.zoom(matriz, 3)
            self.imagen = plt.imshow(data, interpolation = 'nearest')
            self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 100, 951, 751))

            MainWindow.resize(1022, 953)
            MainWindow.setMinimumSize(QtCore.QSize(1020, 853))
            MainWindow.setMaximumSize(QtCore.QSize(1022, 853))

            self.titleLabel.setGeometry(QtCore.QRect(425, 10, 311, 71))
            self.label.setGeometry(QtCore.QRect(740, 18, 270, 61))
            self.spinBox.setGeometry(QtCore.QRect(45, 123, 48, 31))
            self.label_2.setGeometry(QtCore.QRect(5, 100, 151, 16))

            self.label_DivisionSensor.setHidden(True)

        elif (self.numberOfPlatforms == 2):
            #self.radioButton.setVisible(True)
            #self.radioButton_1.setVisible(True)
            #self.radioButton_2.setVisible(False)

            self.pushButton.setVisible(True)
            self.pushButton_1.setVisible(True)
 #           self.pushButton_3.setVisible(False)

            #self.radioButton_2.setVisible(False)
            self.pushButton.setStyleSheet("background-color: green; border-radius: 10px;")
            self.pushButton_1.setStyleSheet("background-color: green; border-radius: 10px;")

            matriz = [[0 for x in range(self.columnas)] for x in range(self.filas)] 
            matriz[0][0] = 255
            matrizSensor2 = [[0 for x in range(self.columnas)] for x in range(self.filas)] 
            matrizCompleta = np.concatenate((matriz,matrizSensor2),axis=1)
            matrizCompleta[0][0] = 255
            data = scipy.ndimage.zoom(matrizCompleta, 3)
            self.imagen = plt.imshow(data, interpolation = 'nearest')
            self.imagen.set_data(data)
            self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 100, 1451, 751))

            MainWindow.resize(1522, 953)
            MainWindow.setMinimumSize(QtCore.QSize(1520, 853))
            MainWindow.setMaximumSize(QtCore.QSize(1522, 853))

            self.spinBox.setGeometry(QtCore.QRect(175, 93, 48, 31))
            self.label_2.setGeometry(QtCore.QRect(35, 100, 151, 16))

            self.titleLabel.setGeometry(QtCore.QRect(675, 10, 311, 71))
            MainWindow.resize(1522, 953)
            self.label.setGeometry(QtCore.QRect(1160, 18, 270, 61))

            self.label_DivisionSensor.setHidden(False)

        elif (self.numberOfPlatforms == 3):

            #self.radioButton.setVisible(True)
            #self.radioButton_1.setVisible(True)
            #self.radioButton_2.setVisible(True)

            self.pushButton.setVisible(True)
            self.pushButton_1.setVisible(True)
 #           self.pushButton_3.setVisible(True)

            self.pushButton.setStyleSheet("background-color: green; border-radius: 10px;")
            self.pushButton_1.setStyleSheet("background-color: green; border-radius: 10px;")

            matriz = [[0 for x in range(self.columnas)] for x in range(self.filas)] 
            matriz[0][0] = 255
            matrizSensor2 = [[0 for x in range(self.columnas)] for x in range(self.filas)] 
            #matrizCompleta = np.concatenate((matriz,matrizSensor2),axis=1)
            matrizCompleta = np.concatenate((matrizSensor2,matriz),axis=1)
            matrizCompleta[0][0] = 255
            data = scipy.ndimage.zoom(matrizCompleta, 3)
            self.imagen = plt.imshow(data, interpolation = 'nearest')
            self.imagen.set_data(data)
            self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 100, 1451, 751))

            MainWindow.resize(1022, 953)
            MainWindow.setMinimumSize(QtCore.QSize(1520, 853))
            MainWindow.setMaximumSize(QtCore.QSize(1522, 853))


    def recibeDatos(self):

        self.dibujarDistribucionPresion(self.vectorDesencriptado)
        #print(time.strftime("%H:%M:%S"))
        threading.Timer(0.01, self.recibeDatos).start()

        
    def dibujarDistribucionPresion(self, matrizDistribucion):
        figure(1)
        
        plt.set_cmap('jet')
        #for row in self.c.execute("SELECT * FROM sensorRigido WHERE `id`='1'"):
        for row in self.c.execute("SELECT * FROM sensorRigido WHERE 1"):
          if row[0] == '1':
              datosSensor1 = row[1]
              sensor1Conectado = row[2]
          if row[0] == '2':
              datosSensor2 = row[1]
              sensor2Conectado = row[2]

        # Los botones se colocan en verde solo cuando se conecta el sensor (estado en la base de datos statusConnection = True)
        if(sensor1Conectado == "True"):
            if(self.green_red_Button_Sensor1 == False):
                self.green_red_Button_Sensor1 = True
                self.connectedSensor.setStyleSheet("background-color: green; color: white; border-radius: 10px")
                self.connectedSensor.setText("Desconectar sensor 1")
                time.sleep(0.1)
                self.pushButton.setStyleSheet("background-color: green; border-style: outset; border-width: 1px; border-radius: 10px; border-color: beige; padding: 6px;")

        if(sensor2Conectado == "True"):
            if(self.green_red_Button_Sensor2 == False):
                self.green_red_Button_Sensor2 = True
                self.connectedSensor_1.setStyleSheet("background-color: green; color: white; border-radius: 10px")
                self.connectedSensor_1.setText("Desconectar sensor 2")
                time.sleep(0.1)
                self.pushButton_1.setStyleSheet("background-color: green; border-style: outset; border-width: 1px; border-radius: 10px; border-color: beige; padding: 6px;")
##      try:
        matrizSensor1 = ast.literal_eval(datosSensor1)
        matrizSensor2 = ast.literal_eval(datosSensor2)

        rotate_imgMatriz1 = scipy.ndimage.rotate(matrizSensor1, -90)
        rotate_imgMatriz2 = scipy.ndimage.rotate(matrizSensor2, -90)

        matriz1espejo = np.array(rotate_imgMatriz1)
        matriz1espejo = matriz1espejo[:,::-1]
        matriz1espejo = matriz1espejo.tolist()

        matriz2espejo = np.array(rotate_imgMatriz2)
        #matriz2espejo = matriz2espejo[::-1,:]
        matriz2espejo = matriz2espejo.tolist()


        matrizCompleta = np.concatenate((matriz1espejo, matriz2espejo), axis=1)
        for i in range(48):
            for j in range(96):
                if matrizCompleta[i][j] > 200:
                    matrizCompleta[i][j] = self.intensityAdjustment

        if self.numberOfPlatforms == 1:
            data = scipy.ndimage.zoom(matriz2espejo, 5)
            self.imagen.set_data(data)
        elif self.numberOfPlatforms == 2:
            dataDatosCompletos = scipy.ndimage.zoom(matrizCompleta, 4)
            self.imagen.set_data(dataDatosCompletos)
        elif self.numberOfPlatforms == 3:
            dataDatosCompletos = scipy.ndimage.zoom(matrizCompleta, 4)
            self.imagen.set_data(dataDatosCompletos)

        
    def conectarSensor1(self):
##        try:
        if(self.sensor1Conectado == False):
            self.sensor1Conectado = True
            self.sqlDataBase()
            threading.Timer(0.01, self.recibeDatos).start()

            self.pushButton.setStyleSheet("background-color: blue; color:white; border-style: outset; border-width: 1px; border-radius: 10px; border-color: beige; padding: 6px;")
            self.connectedSensor.setStyleSheet("background-color: blue; color: white; border-radius: 10px")
            self.connectedSensor.setText("Connecting ...")

            self.t = threading.Thread(target = recvPlataforma1.Ui_MainWindow, args=(self.UDP_IP1, self.UDP_PORT1, self.UDP_IP_CLIENT1, self.UDP_PORT_CLIENT1, self.idSensor1,))
            self.t.IsBackground = True;
            self.t.start()

            self.msg.exec_()

        else:
            try:
                self.c.execute("UPDATE `sensorRigido` SET `connectionStatus` = '%s' WHERE `id`='1'" % 'False')

                self.sensor1Conectado = False
                self.pushButton.setStyleSheet("background-color: red; border-style: outset; border-width: 1px; border-radius: 10px; border-color: beige; padding: 6px;")
                self.connectedSensor.setStyleSheet("background-color: red; color: white; border-radius: 10px")
                self.connectedSensor.setText("Connect 1")
                self.green_red_Button_Sensor1 = False
            except:
                pass
                
            self.conn.commit()


    def conectarSensor2(self):
##        try:
        if(self.sensor2Conectado == False):
            self.sensor2Conectado = True
            self.sqlDataBase()
            threading.Timer(0.01, self.recibeDatos).start()

            self.pushButton_1.setStyleSheet("background-color: blue; border-style: outset; border-width: 1px; border-radius: 10px; border-color: beige; padding: 6px;")
            self.connectedSensor_1.setStyleSheet("background-color: blue; color: white; border-radius: 10px")
            self.connectedSensor_1.setText("Connecting ...")

            self.s = threading.Thread(target = recvPlataforma1.Ui_MainWindow, args=(self.UDP_IP2, self.UDP_PORT2, self.UDP_IP_CLIENT2, self.UDP_PORT_CLIENT2, self.idSensor2,))
            self.s.IsBackground = True;
            self.s.start()

            self.msg.exec_()

        else:
            try:
                self.c.execute("UPDATE `sensorRigido` SET `connectionStatus` = '%s' WHERE `id`='2'" % 'False')

                self.sensor2Conectado = False
                self.pushButton_1.setStyleSheet("background-color: red; border-style: outset; border-width: 1px; border-radius: 10px; border-color: beige; padding: 6px;")
                self.connectedSensor_1.setStyleSheet("background-color: red; color: white; border-radius: 10px")
                self.connectedSensor_1.setText("Connect 2")
                self.green_red_Button_Sensor2 = False
            except:
                pass
                
            self.conn.commit()
                      

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet('QMainWindow{background-color: #222222; border:2px solid black;}')
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

