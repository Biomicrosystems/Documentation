# -*- coding: utf-8 -*-

import socket
import os
from requests import get
from time import sleep

#ip = get('https://api.ipify.org').text
#print 'My public IP address is:', ip

#h = socket.gethostname()
#ip=socket.gethostbyname(h)

s = socket.socket()
host = '192.168.0.18'
nombre = f = ''
port = 8081
videoFile = 'mkv'
dataFile = 'txt'
done = False
out = False
initialize = True
s.connect((host, port))
while True:
    try:
        print(s.recv(1024))
        if initialize:
        	print('\n\rValid data types: "TXT, PNG, CSV"\n\r.TXT is default for remote access\n\rVideo data types: "MP4, MKV"\n\r.MKV is default for remote access\n\n\rMAP (color map 640x480),\nFULLSCREEN (full screen 640x480),\nI_VIDEO (start video recording),\nD_VIDEO (stop video recording),\nV_EXPORT (export last video recorded)\n\n\rTEMP (change to interpolation)\n\rVALUES (change to sensor values), \n\rI_DATOS (start data collection),\nD_DATOS (stop data collection),\nD_EXPORT (export last data collected)\n\n\rMINTEMP## (change the lower limit), \n\rMAXTEMP## (change the upper limit),\n\rSERIALxxx (send xxx through Arduino serial)\n\n\rROOT for folder change\n\rEXPORT change export file\n\rC_EXIT (exit client, server running)\n\rS_EXIT (exit client, server shutdown)\n\rHELP to show again\n')
        	s.send(str.encode('TXT'))
        	print('Data extension changed to TXT as per default')
        	initialize = False
        	print(s.recv(1024))
        b = str.encode(raw_input('Waiting for Command: '))
        if b != 'HELP':
	        s.send(b)
	        if b == 'MP4':
			videoFile = 'mp4'
			print('Video extension changed to MP4')
		elif b == 'MKV':
			videoFile = 'mkv'
			print('Video extension changed to MKV')
	       	elif b == 'TXT':
			dataFile = 'txt'
			print('Data extension changed to TXT')
		elif b == 'CSV':
			dataFile = 'csv'
			print('Data extension changed to CSV')
		elif b == 'PNG':
			dataFile = 'png'	
			print('Data extension changed to PNG')
			
		elif b == 'V_EXPORT':
			videoFile = str(s.recv(1024)).lower()
			while(True):
				try:
					nombre = str(raw_input('Nombre del archivo:')).strip()
					nombre = (nombre + '.' + videoFile).strip()
					print(nombre)
					f = open(nombre,'w')
					break
				except Exception as e:

					print(e)
					#print('Error parcing the file, try again')
			l = s.recv(1024)
			while(not out):
				f.write(l)
				if done:
					break
				l = s.recv(1024)
				if(str(l).find('Done') > 0):
					done = True
			done = False
			f.flush()
			f.close()
		elif b == 'D_EXPORT':
			dataFile = str(s.recv(1024)).lower()
			while(True):
				try:
					nombre = str(raw_input('Nombre del archivo:')).strip()
					nombre = (nombre + '.' + dataFile).strip()
					print(nombre)
					f = open(nombre,'w')
					break
				except Exception as e:
					print(e)
			l = s.recv(1024)
			while(not out):
				f.write(l)
				if done:
					break
				l = s.recv(1024)
				if(str(l).find('Done') > 0):
					done = True
			done = False
			f.flush()
			f.close()
		elif b == 'C_EXIT':
			print('Disconnected from ' + host)
			sleep(5)
			s.close()
			break
		elif b == 'S_EXIT':
			print('Server: '+ host + ' disconnected')
			sleep(5)
			s.close()
			break
        else:
        	print('\n\rValid data types: "TXT, PNG, CSV"\n\r.TXT is default for remote access\n\rVideo data types: "MP4, MKV"\n\r.MKV is default for remote access\n\n\rMAP (color map 640x480),\nFULLSCREEN (full screen 640x480),\nI_VIDEO (start video recording),\nD_VIDEO (stop video recording),\nV_EXPORT (export last video recorded)\n\n\rTEMP (change to interpolation)\n\rVALUES (change to sensor values), \n\rI_DATOS (start data collection),\nD_DATOS (stop data collection),\nD_EXPORT (export last data collected)\n\n\rMINTEMP## (change the lower limit), \n\rMAXTEMP## (change the upper limit),\n\rSERIALxxx (send xxx through Arduino serial)\n\n\rROOT for folder change\n\rEXPORT change export file\n\rC_EXIT (exit client, server running)\n\rS_EXIT (exit client, server shutdown)\n\rHELP to show again\n')
    except Exception as e:
    	print(e)
    	s.close()
        break
s.close()

