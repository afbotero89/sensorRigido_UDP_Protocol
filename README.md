# sensorRigido_UDP_Protocol
Librerias: PyQt5, matplotlib, numpy, scipy.ndimage


Ejecucion 1 plataforma rigida
Parametros: ipPC puertoPC ipModuloWifi puertoModuloWifi idSensor=1
Comunicacion: python3 recvPlataforma1.py 192.168.0.125 10000 192.168.0.150 2233 1
Visualizacion: python3 appRigido1Sensor.py

Ejecucion 2 plataformas rigidas
Parametros: ipPC puertoPC ipModuloWifi puertoModuloWifi idSensor=2
python3 recvPlataforma1.py 192.168.0.125 10000 192.168.0.150 2233 1 & python3 recvPlataforma1.py 192.168.0.125 10001 192.168.0.151 2233 2
Visualizacion: python3 appRigido2Sensores.py
