# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rigidoBotonesConexion.ui'
#
# Created by: GIBIC group
#
# WARNING! All changes made in this file will be lost!


import socket
import binascii
import scipy.ndimage
import sys, struct
#from pylab import *
import time
import sqlite3


maxint = 2 ** (struct.Struct('i').size * 8 - 1) - 1
sys.setrecursionlimit(maxint)

class Ui_MainWindow(object):
    def __init__(self, UDP_IP, UDP_PORT, UDP_IP_CLIENT, UDP_PORT_CLIENT, idSensor):
        print("init")
        self.UDP_IP = UDP_IP
        self.UDP_PORT = UDP_PORT
        self.UDP_IP_CLIENT = UDP_IP_CLIENT
        self.UDP_PORT_CLIENT = UDP_PORT_CLIENT
        self.idSensor = idSensor

        self.vectorDatosDistribucionPresion = []
        self.vectorDesencriptado = []
        self.iniciaTramaDeDatos = False
        self.columnas = 48;
        self.filas = 48;

        self.sensorConnectionStatus = False
        self.connectionRequest = False
        self.conectarSensor()

    # socketConnection: funcion para gestionar la conexion con el sensor rigido      
    def socketConnection(self):
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        print("escuchando...", self.UDP_IP, self.UDP_PORT)
        self.s.bind((self.UDP_IP, self.UDP_PORT))
        #self.s.listen(1)
        #self.sc, self.addr = self.s.accept()
        self.campoSensor1Creado = False
        self.s.settimeout(1)
        while True:            
            time.sleep(2)
            self.s.sendto(bytes('*','utf-8'), (self.UDP_IP_CLIENT, self.UDP_PORT_CLIENT))
            try:
                buf = self.s.recv(10)
                print(buf)
                if(len(buf)>5):
                    self.s.sendto(bytes('*','utf-8'), (self.UDP_IP_CLIENT, self.UDP_PORT_CLIENT))
                    break
            except:
                print("Time out error")
            print("conecto")
        self.s.settimeout(2)
        self.connectionRequest = False
        self.sensorConnectionStatus = True
        self.sqlDataBase()
    
    # sqlDataBase: Funcion para configurar y gestionar la base de datos 
    def sqlDataBase(self):
        print('sql database')
        self.conn = sqlite3.connect('distribucionPresionSensorRigido.db', timeout=10)
        self.c = self.conn.cursor()
        #self.c.execute("DELETE FROM `sensorSuperior` WHERE 1")
        # Create table
        self.c.execute('''CREATE TABLE IF NOT EXISTS sensorRigido
                     (id text, data real, connectionStatus text)''')
        # Insert a row of data
        for row in self.c.execute("SELECT * FROM sensorRigido WHERE 1"):
            if row[0] == self.idSensor:
                self.campoSensor1Creado = True

        if self.campoSensor1Creado == False:
            self.campoSensor1Creado = True
            self.c.execute("INSERT INTO sensorRigido VALUES ('%s','initValue sensor 1','True')" % self.idSensor)
        self.c.execute("UPDATE `sensorRigido` SET `connectionStatus` = '%s' WHERE `id`='%s'" % ('True',self.idSensor))
        self.conn.commit()
    
    # desencriptarVector: Funcion para la desencriptacion del vector segun el protocolo de comunicacion
    # parametros: vector, este vector es el que se recibe por medio del modulo wifi    
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
                            if fil >= self.filas:
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

    # recibeDatos: funcion que hace lectura del buffer y llama las funciones para descencriptar y insertar datos en la base de datos.   
    def recibeDatos(self):
 #       self.sc.settimeout(None)
        while True:
            try:
                for row in self.c.execute("SELECT * FROM sensorRigido WHERE `id`='%s'" % self.idSensor):
                    if row[2] == 'True':
                        self.sensorConnectionStatus = True
                        self.connectionRequest = True
                    else:
                        print('cierra conexion')
                        self.sensorConnectionStatus = False
                        self.connectionRequest = False
                        #self.sc.close()
                        self.s.close()
                        break
                        
                time.sleep(0.05)
                if self.sensorConnectionStatus == True:
      
                    buf = self.s.recv(6000)
                    
                    info = [buf[i:i+1] for i in range(0, len(buf), 1)]
                    #try:
                    for i in info:
                        valorDecimal = int(binascii.hexlify(i),16)
                        
                        if self.iniciaTramaDeDatos == False:
                          self.vectorDatosDistribucionPresion.append(valorDecimal)
                          
                          # Segun el protocolo establecido, el 255 indica fin de trama, los dos datos anteriores son la longitud de los datos (cheksum)
                          # van en dos bytes, por tal razon es necesario la conversion self.numeroBytes = self.primerByte*255 + self.segundoByte
                          if valorDecimal == 255:
                            self.primerByte = self.vectorDatosDistribucionPresion[len(self.vectorDatosDistribucionPresion) - 3]
                            self.segundoByte = self.vectorDatosDistribucionPresion[len(self.vectorDatosDistribucionPresion) - 2]
                            self.numeroBytes = self.primerByte*255 + self.segundoByte

                            # El numero de bytes enviado por el sensor debe ser igual al desencriptado (checksum)
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
                                self.s.sendto(bytes('*','utf-8'), (self.UDP_IP_CLIENT, self.UDP_PORT_CLIENT))
                                #self.sc.send(('*').encode())
                                break
                            else:
                                self.vectorDatosDistribucionPresion = []
                                info = []
                                self.iniciaTramaDeDatos = False
                                self.s.sendto(bytes('*','utf-8'), (self.UDP_IP_CLIENT, self.UDP_PORT_CLIENT))
                                #self.sc.send(('*').encode())
                                break

                        if valorDecimal == 255 and self.iniciaTramaDeDatos == False:
                            self.s.sendto(bytes('*','utf-8'), (self.UDP_IP_CLIENT, self.UDP_PORT_CLIENT))
                            #self.sc.send(('*').encode())
                            self.iniciaTramaDeDatos = True
                    self.s.sendto(bytes('*','utf-8'), (self.UDP_IP_CLIENT, self.UDP_PORT_CLIENT))
                    #self.sc.send(('*').encode())
                else:
                    if self.connectionRequest == True:
                        self.socketConnection()
                    print("sensor desconectado")
            except:
                pass
    # Funcion para insertar matriz desencriptada en la base de datos.
    # Parametros: matrizDistribucion, matriz desencriptada deacuerdo con el protocolo.    
    def dibujarDistribucionPresion(self, matrizDistribucion):

        maximoValor = 0
          
        for i in range(self.filas):

            for j in range(self.columnas):

                matrizDistribucion[i][j] = matrizDistribucion[i][j]*1

                if matrizDistribucion[i][j] > 200:
                    pass
                    #matrizDistribucion[i][j] = 240
                if matrizDistribucion[i][j] >= maximoValor:
                    maximoValor = matrizDistribucion[i][j]

          
        data = scipy.ndimage.zoom(matrizDistribucion, 1)
        print("inserta datos base de datos")
        #self.c.execute("UPDATE `sensorRigido` SET `data`= '%s', `connectionStatus` = '%s' WHERE `id`='1'" % (matrizDistribucion,'True'))
        self.c.execute("UPDATE `sensorRigido` SET `data`= '%s' WHERE `id`='%s'" % (matrizDistribucion, self.idSensor))
        self.conn.commit()

    def conectarSensor(self):
        #try:
            self.socketConnection()
            self.recibeDatos()
            #threading.Timer(0.01, self.recibeDatos()).start()
            print("conecta conecta")
        #except:
            #print("No conecta")

