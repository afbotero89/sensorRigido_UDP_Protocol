# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rigidoBotonesConexion.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!


import socket
import sys
import binascii
import threading
import numpy as np
import socket
#import scipy.ndimage
import sys, struct
#from pylab import *
import time
import sqlite3
#ion()

maxint = 2 ** (struct.Struct('i').size * 8 - 1) - 1
sys.setrecursionlimit(maxint)

class Ui_MainWindow(object):
    def __init__(self):
        print("init")
        self.vectorDatosDistribucionPresion = []
        self.vectorDesencriptado = []
        self.iniciaTramaDeDatos = False
        self.columnas = 48;
        self.filas = 48;
        matriz = [[0 for x in range(self.columnas)] for x in range(self.filas)] 
        matriz[0][0] = 255
        self.sensorConnectionStatus = False
        self.connectionRequest = False
        #self.cronometro = tiemposDeExposicion.Cronometro()
        #self.interfazTiempos = interfazTiemposExposicionSensor2.interfazTiemposExposicion()
            
    def socketConnection(self):
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.s.settimeout(0.5)
        #self.s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ip = "192.168.0.124"
        self.port = 10000
        self.s.bind((self.ip,self.port))
        self.s.listen(1)
        print('escuchando ..', self.ip, self.port)
        self.sc, self.addr = self.s.accept()
        self.campoSensor1Creado = False
        for i in range(3):            
            time.sleep(2)
            self.sc.send(('*').encode())
            print("conecto")
        self.connectionRequest = False
        self.sensorConnectionStatus = True
        self.sqlDataBase()
        self.c.execute("UPDATE `sensorRigido` SET `connectionStatus` = '%s' WHERE `id`='2'" % 'True')
        self.recibeDatos()
        
        
    def sqlDataBase(self):
        print('sql database sensor 2')
        self.conn = sqlite3.connect('distribucionPresionSensorRigido.db', timeout=10)
        self.c = self.conn.cursor()
        #self.c.execute("DELETE FROM `sensorSuperior` WHERE 1")
        # Create table
        self.c.execute('''CREATE TABLE IF NOT EXISTS sensorRigido
                     (id text, data real, connectionStatus text)''')
        # Insert a row of data
        #self.c.execute("INSERT INTO sensorRigido VALUES ('2','initValue2')")
        for row in self.c.execute("SELECT * FROM sensorRigido WHERE 1"):
            if row[0] == '2':
                self.campoSensor1Creado = True

        if self.campoSensor1Creado == False:
            self.campoSensor1Creado = True
            self.c.execute("INSERT INTO sensorRigido VALUES ('2','initValue sensor 2','True')")
        self.conn.commit()
        
    def desencriptarVector(self,vector):
        n = len(vector);
        fil = 0;
        col = 0;
        matriz = [[0 for x in range(self.columnas)] for x in range(self.filas)];
        banderacero = 0;
        for x in range(0, n):
            datos = vector[x];
            if datos == 0:
                banderacero = 1;
            elif datos == 255:
                return matriz;
            else:
                if banderacero == 1:
                    for k in range (0, datos):
                        if col == self.columnas:
                            col = 0;
                            fil = fil + 1;
                            if fil > self.filas:
                                return matriz;
                            matriz[fil][col] = 0;
                        col = col + 1;
                else:
                    if col >= self.columnas:
                        col = 0;
                        fil = fil + 1;
                        if fil >= self.filas:
                            return matriz;
                    matriz[fil][col] = datos;
                    col = col + 1;
                banderacero = 0;
                
    def recibeDatos(self):
 #       self.sc.settimeout(None)
        while True:

            for row in self.c.execute("SELECT * FROM sensorRigido WHERE 1"):
                print(row[0],row[2])
            for row in self.c.execute("SELECT * FROM sensorRigido WHERE `id`='2'"):
                
                if row[2] == 'True':
                    self.connectionRequest = True
                else:
                    self.sensorConnectionStatus = False
                    self.connectionRequest = False
                    self.sc.close()
                    self.s.close()
                    print('cierra conexion')
            if self.sensorConnectionStatus == True:
                buf = self.sc.recv(1000)
         #       self.sc.settimeout(0)
                print(time.strftime("%H:%M:%S"))
                info = [buf[i:i+1] for i in range(0, len(buf), 1)]
                #try:
                for i in info:
                    valorDecimal = int(binascii.hexlify(i),16)
                    
                    if self.iniciaTramaDeDatos == False:
                      self.vectorDatosDistribucionPresion.append(valorDecimal)
                      
                      if valorDecimal == 255:
                        self.primerByte = self.vectorDatosDistribucionPresion[len(self.vectorDatosDistribucionPresion) - 3]
                        self.segundoByte = self.vectorDatosDistribucionPresion[len(self.vectorDatosDistribucionPresion) - 2]
                        self.numeroBytes = self.primerByte*255 + self.segundoByte

                        if(self.numeroBytes == len(self.vectorDatosDistribucionPresion) - 3):

                            self.vectorDatosDistribucionPresion=self.vectorDatosDistribucionPresion[:len(self.vectorDatosDistribucionPresion)-1]
                            self.vectorDatosDistribucionPresion=self.vectorDatosDistribucionPresion[:len(self.vectorDatosDistribucionPresion)-1]
                            self.vectorDatosDistribucionPresion=self.vectorDatosDistribucionPresion[:len(self.vectorDatosDistribucionPresion)-1]
                            self.vectorDatosDistribucionPresion.append(255)
                            self.vectorDesencriptado = self.desencriptarVector(self.vectorDatosDistribucionPresion)
                            self.dibujarDistribucionPresion(self.vectorDesencriptado)
                            self.vectorDatosDistribucionPresion = []
                            info = []
                            self.iniciaTramaDeDatos = False
                            self.sc.send(('*').encode())
                            break
                        else:
                            self.vectorDatosDistribucionPresion = []
                            info = []
                            self.iniciaTramaDeDatos = False
                            self.sc.send(('*').encode())
                            break

                    if valorDecimal == 255 and self.iniciaTramaDeDatos == False:
                        self.sc.send(('*').encode())
                        self.iniciaTramaDeDatos = True
                self.sc.send(('*').encode())
            else:
                if self.connectionRequest == True:
                    self.socketConnection()
                print("sensor desconectado")

        
    def dibujarDistribucionPresion(self, matrizDistribucion):

##      
      for i in range(self.filas):
        for j in range(self.columnas):
            matrizDistribucion[i][j] = matrizDistribucion[i][j]*2
##
            if matrizDistribucion[i][j] > 200:
                matrizDistribucion[i][j] = 240
##            if matrizDistribucion[i][j] >= maximoValor:
##                maximoValor = matrizDistribucion[i][j]
      #print(maximoValor)
      
 #     data = scipy.ndimage.zoom(matrizDistribucion, 1)
      #self.c.execute("UPDATE `sensorRigido` SET `data`= '%s', `connectionStatus` = '%s' WHERE `id`='2'" % (matrizDistribucion,'True'))
      self.c.execute("UPDATE `sensorRigido` SET `data`= '%s' WHERE `id`='2'" % matrizDistribucion)
      #c.execute("UPDATE `tablaprueba` SET `data`= '%s', `connectionStatus` = '%s' WHERE `id`='1'" % ('datos modificado','false'))
      #self.conn.commit()
      #self.c.execute("UPDATE `sensorRigido` SET `data`= '%s' WHERE `id`='2'" % matrizDistribucion)
      self.conn.commit()


    def conectarSensor(self):
        #try:
            self.socketConnection()
            self.recibeDatos()
            #threading.Timer(0.01, self.recibeDatos()).start()
            print("conecta conecta")
        #except:
            #print("No conecta")


if __name__ == "__main__":
    import sys
    ui = Ui_MainWindow()
    ui.conectarSensor()
    #ui.recibeDatos()

