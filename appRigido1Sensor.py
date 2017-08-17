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
import ast
ion()

maxint = 2 ** (struct.Struct('i').size * 8 - 1) - 1
sys.setrecursionlimit(maxint)

class Ui_MainWindow(object):
    def __init__(self):
        print("init")
        self.fig = plt.figure(facecolor='#222222',figsize=(9,9))
        self.fig.set_size_inches(9,9)
        self.ax = plt.Axes(self.fig, [0., 0., 1., 1.])
        self.ax.set_axis_off()
        self.fig.add_axes(self.ax)
        self.fig.canvas.draw()
        #self.fig.canvas.toolbar.pack_forget()
        #plt.show(block=False)
        self.vectorDatosDistribucionPresion = []
        self.vectorDesencriptado = []
        self.iniciaTramaDeDatos = False
        self.columnas = 48;
        self.filas = 48;
        self.era = []
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
        self.ax = plt.gca()

        divider = make_axes_locatable(self.ax)
        cax = divider.append_axes("right", size="3%", pad=0.05)

        self.cbar = self.fig.colorbar(self.ax.imshow(matriz), ticks=[5,125,250],cax=cax)
        self.cbar.ax.set_yticklabels(['Baja','Medio','Alto'])
        self.cbar.ax.tick_params(labelcolor='w', labelsize=12)
        #divider = make_axes_locatable(plt.gca())
        #cax = divider.append_axes("right","5%",pad="3%")
        #plt.colorbar(plt.imshow(matrizCompleta),cax=cax)
        
        self.initData = scipy.ndimage.zoom(matriz, 3)
        #self.contour = plt.contour(data)
        
        self.imagen = self.ax.imshow(self.initData, interpolation = 'nearest')
        self.contador = 0
        self.contour_axis = plt.gca()
        self.sensorConectado = False
        self.defaultNumberOfPlatforms = 1
        self.numberOfPlatforms = 2
        self.intensityAdjustment = 240

        # Parametros de comunicacion
        self.UDP_IP = "192.168.0.124"
        self.UDP_PORT = 10000

        self.UDP_IP_CLIENT = "192.168.0.107"
        self.UDP_PORT_CLIENT = 2233

        self.idSensor = "1"
        self.visualizarPresion = False

        self.green_red_Button = False

        self.activePressureVectors = False
        
        #plt.gca().invert_yaxis()
            
    def sqlDataBase(self):
        
        self.conn = sqlite3.connect('distribucionPresionSensorRigido.db', check_same_thread=False, timeout=10)
        self.c = self.conn.cursor()
        
    def setupUi(self, MainWindow):
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(922, 953)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(920, 853))
        MainWindow.setMaximumSize(QtCore.QSize(922, 853))
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
        self.label.setGeometry(QtCore.QRect(650, 18, 280, 61))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("img/logoGIBIC.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        self.titleLabel = QtWidgets.QLabel(self.centralWidget)
        self.titleLabel.setGeometry(QtCore.QRect(375, 10, 211, 71))
        self.titleLabel.setText("Sensor de presión")
        self.titleLabel.setStyleSheet("background-color: black; color:white; font size: 28pt; font-size: 22pt;")
        self.titleLabel.setScaledContents(True)
        self.titleLabel.setObjectName("titleLabel")

        self.gridLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(-70, 90, 1051, 751))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        
        canvas = FigureCanvas(self.fig)
        self.gridLayout.addWidget(canvas)
            
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")

        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setText("Conectando sensor")
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok) 
        self.msg.setGeometry(QtCore.QRect(575, 425, 1051, 751))

        self.msg1 = QtWidgets.QMessageBox()
        self.msg1.setIcon(QtWidgets.QMessageBox.Information)
        self.msg1.setText("Sensor desconectado")
        self.msg1.setStandardButtons(QtWidgets.QMessageBox.Ok) 

        # Push button
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setStyleSheet("background-color: red; border-style: outset; border-width: 1px; border-radius: 10px; border-color: beige; padding: 6px;")
        self.pushButton.setGeometry(QtCore.QRect(165, 35, 20, 20))
        self.pushButton.setObjectName("pushButton")


        self.connectedSensor = QtWidgets.QPushButton(self.centralWidget)
        self.connectedSensor.setStyleSheet("background-color: red; color: white; border-radius: 10px")
        self.connectedSensor.setGeometry(QtCore.QRect(10, 30, 140, 32))
        self.connectedSensor.setObjectName("connectedSensor")

        self.pushButtonPressureVector = QtWidgets.QPushButton(self.centralWidget)
        self.pushButtonPressureVector.setStyleSheet("background-color: red; border-style: outset; border-width: 1px; border-radius: 10px; border-color: beige; padding: 6px;")
        self.pushButtonPressureVector.setGeometry(QtCore.QRect(200, 30, 120, 32))
        self.pushButtonPressureVector.setObjectName("pushButtonPressureVector")
        self.pushButtonPressureVector.setText("ON Vectors")

        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GIBIC group"))
        self.pushButton.setText(_translate("MainWindow", ""))
        self.connectedSensor.clicked.connect(self.conectarSensor)
        self.pushButtonPressureVector.clicked.connect(self.pressureVectors)
        
        self.connectedSensor.setText(_translate("MainWindow", "Conectar sensor"))
        #self.label_2.setText(_translate("MainWindow", "Número de plataformas:"))

        self.t = threading.Thread(target = self.recibeDatos)
        self.t.IsBackground = True;
        self.t.start()
        #self.groupRadioButton.buttonClicked[int].connect(self.ButtonGroupClicked)

    #def ButtonGroupClicked(self,clicked):
        #print("radio button clicked",clicked*(-1))
    def pressureVectors(self):
        if(self.activePressureVectors == False):
            self.activePressureVectors = True
            self.pushButtonPressureVector.setStyleSheet("background-color: green; border-style: outset; border-width: 1px; border-radius: 10px; border-color: beige; padding: 6px;")
            self.pushButtonPressureVector.setText("ON Vectors")
        else:
            self.activePressureVectors = False
            self.pushButtonPressureVector.setStyleSheet("background-color: red; border-style: outset; border-width: 1px; border-radius: 10px; border-color: beige; padding: 6px;")
            self.pushButtonPressureVector.setText("OFF Vectors")

    def recibeDatos(self):
        while True:
            self.dibujarDistribucionPresion(self.vectorDesencriptado)
            time.sleep(0.05) 
        #print(time.strftime("%H:%M:%S"))
        #threading.Timer(0.1, self.recibeDatos).start()

        
    def dibujarDistribucionPresion(self, matrizDistribucion):

        try:
            #for row in self.c.execute("SELECT * FROM sensorRigido WHERE `id`='1'"):
            if(self.visualizarPresion == True):
                for row in self.c.execute("SELECT * FROM sensorRigido WHERE 1"):
                    if row[0] == '1':
                        datosSensor1 = row[1]
                    if row[0] == '2':
                        datosSensor2 = row[1]
                    sensorConectado = row[2]
                   
                if sensorConectado == "True":

                    if(self.green_red_Button == False):
                        self.green_red_Button = True
                        self.connectedSensor.setStyleSheet("background-color: green; color: white; border-radius: 10px")
                        self.connectedSensor.setText("Desconectar sensor")
                        time.sleep(0.1)
                        self.pushButton.setStyleSheet("background-color: green; border-style: outset; border-width: 1px; border-radius: 10px; border-color: beige; padding: 6px;")

                    matrizSensor2 = ast.literal_eval(datosSensor1)
                    COP = ast.literal_eval(row[4])
                    old = ast.literal_eval(row[3])

                    del COP[2]
                    del old[2]
                    for i in range (0,2):
                        if (old != [0, 0] and COP!=[0, 0]):
                            if i == 1:
                                COP[i] = (47-COP[i])*3
                                old[i] = (47-old[i])*3
                            else:
                                COP[i] = (COP[i])*3
                                old[i] = (old[i])*3
                    #rotate_imgMatriz1 = scipy.ndimage.rotate(matrizSensor1, 90)
                    rotate_imgMatriz2 = scipy.ndimage.rotate(matrizSensor2, 180)

                    matriz2espejo = np.array(rotate_imgMatriz2)
                    matriz2espejo = matriz2espejo[::-1,:]
                    matriz2espejo = matriz2espejo.tolist()

                    matrizCompleta = np.concatenate((matriz2espejo, matriz2espejo), axis=1)
                    for i in range(48):
                        for j in range(96):
                            if matrizCompleta[i][j] > 200:
                                matrizCompleta[i][j] = self.intensityAdjustment

                    if(self.activePressureVectors == False):
                        dataDatosCompletos = scipy.ndimage.zoom(matriz2espejo, 5)
                        self.imagen.set_data(dataDatosCompletos)
                    else:    
                        dataDatosCompletos = scipy.ndimage.zoom(matriz2espejo, 5)
                        
                        self.imagen.set_data(dataDatosCompletos)
                        if (old != [0, 0] and COP!=[0, 0]):
                            self.era.append(self.ax.plot([old[1],COP[1]],[old[0],COP[0]],color = 'white', marker = 'o',linewidth=3.0))

                            if (len(self.era)>1):
                                self.ax.lines.pop(0)

                    print("plot matriz", sensorConectado, self.activePressureVectors)

                    try:
                        if COP == [0,0]:
                            self.ax.lines.pop(0)
                            self.era = []
                    except:
                        pass

                    figure(1)

                    plt.set_cmap('jet')                        
            else:
                pass
        except:
            pass
      
    def conectarSensor(self):
##        try:
        if(self.sensorConectado == False):
            self.sensorConectado = True
            self.sqlDataBase()
            try:

                self.connectedSensor.setText("Conectando...")
                self.connectedSensor.setStyleSheet("background-color: blue; color: white; border-radius: 10px")
                self.pushButton.setStyleSheet("background-color: blue; border-style: outset; border-width: 1px; border-radius: 10px; border-color: beige; padding: 6px;")
                self.visualizarPresion = True

                self.t = threading.Thread(target = recvPlataforma1.Ui_MainWindow, args=(self.UDP_IP, self.UDP_PORT, self.UDP_IP_CLIENT, self.UDP_PORT_CLIENT, self.idSensor,))
                self.t.IsBackground = True;
                self.t.start()

            except:
                pass
            print("Sensor conectado")
            self.conn.commit()

            #self.msg.exec_()

        else:
            self.sensorConectado = False
            try:
                self.c.execute("UPDATE `sensorRigido` SET `connectionStatus` = '%s' WHERE `id`='1'" % 'False')
                self.c.execute("UPDATE `sensorRigido` SET `connectionStatus` = '%s' WHERE `id`='2'" % 'False')

                self.pushButton.setStyleSheet("background-color: red; border-style: outset; border-width: 1px; border-radius: 10px; border-color: beige; padding: 6px;")
                self.connectedSensor.setStyleSheet("background-color: red; color: white; border-radius: 10px")

                self.connectedSensor.setText("Conectar sensor")
                self.visualizarPresion = False
                self.green_red_Button = False
            except:
                pass    
            self.conn.commit()
            print("sensor desconectado")
                      

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet('QMainWindow{background-color: #222222; border:2px solid black;}')
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

