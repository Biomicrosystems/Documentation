#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################################Librerias

import serial
import pygame
import select
import socket
import re
import os
import math
import time
import threading
import numpy as np
import glob
import csv
import subprocess
import signal
import spidev
import RPi.GPIO as GPIO
import Tkinter, tkFileDialog
from scipy.interpolate import griddata
from scipy.stats import linregress
from pygame.locals import *
from time import time
from colour import Color
from os import listdir
from botonesPrincipales import *
from Adafruit_AMG88xx import Adafruit_AMG88xx
from time import sleep
from requests import get

########################################################################CLASE PARA INPUTBOX

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = YELLOW
        self.text = text
        self.txt_surface = textFont_temp.render(text, True, self.color)
        self.active = False
        self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
        self.ser.flush()
        self.line = ''

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = AZUL if self.active else YELLOW
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = bytes(self.text+'\n')
                    self.ser.write(self.text)
                    self.line = self.ser.readline().decode('utf-8').rstrip()
                    print(self.line)
                    sleep(1)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = textFont_temp.render(self.text, True, self.color)
    
    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, lcd):
        lcd.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(lcd, self.color, self.rect, 2)

########################################################################Atributos 

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

calib_scale240 = float(240)/3788   # Likely about 285
calib_scale320 = float(320)/3777   # Likely about 384
calib_offset240 = calib_scale240 * 180   # Likely about 28
calib_offset320 = calib_scale320 * 318   # Likely about 25

########################################################################Variables del sistema

salirMainScrn = False
corriendoMainScrn = False
salir = False
imprimirTem = True
grabandoCSV = False
salirGrabacionCSV = True
grabandoVideo = False
grabarVideo = False
configurar = False
configurando = False
confiMax = False
confiMin = False
confiCal = False
configurandoCal = False
tomaHabilitada = True
archivoVideoNuevo = ''
archivoDatosNuevo = ''

calX = []
calY = []

promedioTem = 0
promedioDatos = 0

box_active = False
input_box = pygame.Rect(79, 185, 82, 31)

color_inactive = (0,0,0)
color_active = pygame.Color('dodgerblue2')

csv_pixels = []
tiempo_inicio_csv = time()

########################################################################Variables de configuración

MINTEMP = 20
MAXTEMP = 30

servidor = False
servidorThread = False
extActual = 'CSV'
extActual2 = 'MKV'
videoCon = 'MAP'
ip = 'N/A'
newCommand = 'N/A'

fileNameLimits = 'source/colorLimits.txt'
fileNameCalibration = 'source/calibration.txt'

try:
    colorFile = open(fileNameLimits,'r')
    colorStr = colorFile.read().split(",")
    colorInt = [int(x) for x in colorStr]
    MINTEMP = colorInt[0]
    MAXTEMP = colorInt[1]
except:
    print("Color por defecto")

xParameter = 0.2959
bParameter = -2.4836
try:
    calibrationFile = open(fileNameCalibration,'r')
    calibrationStr = calibrationFile.read().split(",")
    calibrationInt = [float(x) for x in calibrationStr]
    xParameter = calibrationInt[0]
    bParameter = calibrationInt[1]
except:
    print("Calibración por defecto")


########################################################################Configuración de colores
#how many color values we can have
COLORDEPTH = 1024
nPixels = 64

os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()
global root

#the list of colors we can choose from
blue = Color("indigo")
colorsList = list(blue.range_to(Color("red"), COLORDEPTH))
FONDO = (32, 30, 32)
BLANCO = (255, 255, 255)
COLOR_TEXTO = (50, 60, 80)
GRIS =(211,211,211)
AZUL = (42, 39, 96)
NEGRO = (0,0,0)
YELLOW = (255, 255, 0)

#create the array of colors
colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in colorsList]
# colorsTrans = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255), 50) for c in colorsList]

#initialize the sensor
sensor = Adafruit_AMG88xx()

points = [(math.floor(ix / 8), (ix % 8)) for ix in range(0, 64)]

grid_x, grid_y = np.mgrid[0:7:32j*float(scalable-0.031), 0:7:32j*float(scalable-0.031)]

########################################################################Configuración de la Pantalla
#Screen is 240x320

scalable = 2

scrn_height = 240*scalable
scrn_width = 320*scalable

#sensor is an 8x8 grid so lets do a square
map_height = min(scrn_height,scrn_width)
map_width = min(scrn_height,scrn_width)

displayPixelWidthCubic = float(map_width) / 30
displayPixelHeightCubic = float(map_height) / 30

displayPixelWidth = map_width / 8
displayPixelHeight = map_height / 8

clock = pygame.time.Clock()
click = False
########################################################################Botones principales
def posBotonRec(pos, dim):
    rec = (pos[0]-dim[0]/2,pos[1]-dim[1]/2 , dim[0], dim[1])
    return rec

def posBotonEsquina(pos, dim):
    rec = [pos[0]-dim[0]/2, pos[1]-dim[1]/2]
    return rec

tam_boton = (scrn_width - map_width)/2
botones=[]
botonesMainScreen(pygame, botones)

botonesConfig = []
botonesSettingScreen(pygame, botonesConfig)

botonesMaximo = []
botonesLimScreen(pygame, botonesMaximo)

botonesCalibracion = []
botonesCalScreen(pygame, botonesCalibracion)

########################################################################Interfaz

#Se crea la pantalla que contendra la interfaz
flags = pygame.DOUBLEBUF | pygame.SRCALPHA
lcd = pygame.display.set_mode((scrn_width, scrn_height), flags)
pygame.display.set_caption('Cámara Térmica')
textFont = pygame.font.SysFont("comicsansms", int(displayPixelWidth/2))
textFont_botones = pygame.font.SysFont("comicsansms", int(tam_boton/3))
textFont_temp = pygame.font.SysFont("comicsansms", int(displayPixelWidth/2.5))
textFont_rango_confi = pygame.font.SysFont("comicsansms", 60)
textFont_rango_cal = pygame.font.SysFont("comicsansms",40 )
textFont_titulo = pygame.font.SysFont("comicsansms", 30)
lcd.fill(BLANCO)
pygame.display.update()

directorios = listdir("/media/pi")
if len(directorios)>0:
    raiz = "/media/pi/" + directorios[0] +"/"
else:
    raiz = "/home/pi/Desktop/Datos_CT/"

raiz = "/home/pi/Desktop/Datos_CT/"

input_box1 = InputBox(220, 80, 400, 50)  

#Funciones
#Guardar variables tlimites
def guardarVariables(var1, var2, archivo):
    file = open(archivo,"w")
    text = str(var1) + "," + str(var2)
    file.write(text)
    file.close()

def regLineal(datX, datY):
    regresion = linregress(datX, datY)
    pendiente = regresion.slope
    corte = regresion.intercept
    return pendiente,corte

def actualizarTemCal(var):
    global text_recV
    var = round(var,2)
    posMenos = botonesCalibracion[2]['pos']
    posMas = botonesCalibracion[3]['pos']
    colorText = color_active if box_active else color_inactive
    textLabelVar = textFont_rango_cal.render(str(var), True, colorText)
    text_recV = textLabelVar.get_rect()
    text_recV.center = ((posMenos[0] + posMas[0]) / 2, (posMenos[1] + posMas[1]) / 2)
    pygame.draw.rect(lcd, BLANCO, input_box)
    lcd.blit(textLabelVar, text_recV)

def dibujar_botones_calibracion():
    lcd.fill(BLANCO)
    for boton in botonesCalibracion:
        if boton['habilitado']:
            lcd.blit(boton['imagen'], boton['rect'])
        else:
            lcd.blit(boton['imagen_dos'], boton['rect'])
    texto = "Calibracion manual"
    textFont_titulo = pygame.font.SysFont("comicsansms", 30)
    textLabel = textFont_titulo.render(texto, True, NEGRO)
    text_rec =  textLabel.get_rect()
    text_rec.center = (180, 25)
    lcd.blit(textLabel, text_rec)

def dibujarBarraColor(posHorizontal):
    widthBar = 10
    heightBar = scrn_height
    for i in range(heightBar):
        pygame.draw.rect(lcd, colors[int(i*(4/scalable))],(posHorizontal+1, heightBar-i, widthBar, 2))
    rango = MAXTEMP - MINTEMP
    nTxtBar = 5
    tam_marcas = rango/float(nTxtBar-1)
    tam_marcas_pixel = map_height/(nTxtBar-1)
    for i in range(nTxtBar):
        txtBar = "- "+str(int(MINTEMP+int(tam_marcas*i)))
        textLabel = textFont_temp.render(txtBar, True, NEGRO)
        lcd.blit(textLabel, (posHorizontal + 12, map_height - tam_marcas_pixel*i -int(displayPixelWidth/3)))
    txt = "- "+str(MAXTEMP)
    textLabel = textFont_temp.render(txt, True, NEGRO)
    lcd.blit(textLabel, (posHorizontal + 12, 1))

def dibujar_botones_configuracion():
    global ip, newCommand, lcd, input_box1, configurar
    for boton in range(0, 13):
        rec = posBotonRec(botonesConfig[boton]['pos'], (85,85))
        pygame.draw.rect(lcd, BLANCO, rec)
        lcd.blit(botonesConfig[boton]['imagen'], botonesConfig[boton]['rect'])
        textLabel = textFont_temp.render(botonesConfig[boton]['texto'][0], True, NEGRO)
        lcd.blit(textLabel, (rec[0]-20, rec[1]+rec[3] - 105))
    if servidor:
        rec = posBotonRec(botonesConfig[13]['pos'], (85,85))
        pygame.draw.rect(lcd, BLANCO, rec)
        lcd.blit(botonesConfig[13]['imagen'], botonesConfig[13]['rect'])
        textLabel = textFont_temp.render(botonesConfig[13]['texto'][0], True, NEGRO)
        lcd.blit(textLabel, (rec[0]-20, rec[1]+rec[3] - 105))
    else:
        rec = posBotonRec(botonesConfig[13]['pos'], (85,85))
        pygame.draw.rect(lcd, BLANCO, rec)
        lcd.blit(botonesConfig[13]['imagen_dos'], botonesConfig[13]['rect'])
        textLabel = textFont_temp.render(botonesConfig[13]['texto'][0], True, NEGRO)
        lcd.blit(textLabel, (rec[0]-20, rec[1]+rec[3] - 105))
    textLabel = textFont_temp.render("Carpeta actual: "+ raiz, True, NEGRO)
    lcd.blit(textLabel, (10, 450))
    textLabel = textFont_temp.render("Extension de archivo de datos:", True, NEGRO)
    lcd.blit(textLabel, (10, 20))
    textLabel = textFont_temp.render(extActual, True, NEGRO)
    lcd.blit(textLabel, (10, 38))
    textLabel = textFont_temp.render("Extension de archivo de video:", True, NEGRO)
    lcd.blit(textLabel, (10, 150))
    textLabel = textFont_temp.render(extActual2 + '/' + videoCon, True, NEGRO)
    lcd.blit(textLabel, (10, 168))
    textLabel = textFont_temp.render('Direccion IP local:', True, NEGRO)
    lcd.blit(textLabel, (470, 400))
    textLabel = textFont_temp.render(ip, True, NEGRO)
    lcd.blit(textLabel, (470, 418))
    textLabel = textFont_temp.render('Configuracion manual:', True, NEGRO)
    lcd.blit(textLabel, (10, 300))
    textLabel = textFont_temp.render('Limites       Regresion', True, NEGRO)
    lcd.blit(textLabel, (10, 320))
    #textLabel = textFont_temp.render(newCommand, True, NEGRO)
    #lcd.blit(textLabel, (470, 436))    
    pygame.display.update()   

def dibujar_botones_rango(texto, var):
    global botonesMaximo, MAXTEMP, MINTEMP
    lcd.fill(GRIS)
    if texto == 'save':
        lcd.blit(botonesMaximo[2]['imagen'], botonesMaximo[2]['rect'])
        lcd.blit(botonesMaximo[5]['imagen'], botonesMaximo[5]['rect'])
    else:
        for boton in range(0, 5):
            lcd.blit(botonesMaximo[boton]['imagen'], botonesMaximo[boton]['rect'])
        posMenos = botonesMaximo[0]['pos']
        posMas = botonesMaximo[1]['pos']
        textLabelVar = textFont_rango_confi.render(str(MAXTEMP), True, NEGRO)
        text_recV = textLabelVar.get_rect()
        text_recV.center = ((posMenos[0] + posMas[0]) / 2, (posMenos[1] + posMas[1]) / 2)
        lcd.blit(textLabelVar, text_recV)
        textLabel = textFont_titulo.render('Tope temperatura maxima', True, NEGRO)
        text_rec =  textLabel.get_rect()
        text_rec.center = (210, 85)
        lcd.blit(textLabel, text_rec)
        posMenos = botonesMaximo[3]['pos']
        posMas = botonesMaximo[4]['pos']
        textLabelVar = textFont_rango_confi.render(str(MINTEMP), True, NEGRO)
        text_recV = textLabelVar.get_rect()
        text_recV.center = ((posMenos[0] + posMas[0]) / 2, (posMenos[1] + posMas[1]) / 2)
        lcd.blit(textLabelVar, text_recV)
        textLabel = textFont_titulo.render('Tope temperatura minima', True, NEGRO)
        text_rec =  textLabel.get_rect()
        text_rec.center = (210, 285)
        lcd.blit(textLabel, text_rec)
        dibujarBarraColor(500)

def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def dibujar_botones_iniciales(lista_botones):
    lcd.fill(BLANCO)
    for boton in lista_botones:
        if boton['selected']:
            lcd.blit(boton['imagen_dos'], boton['rect'])
            textBoton = boton['texto2']
        else:
            lcd.blit(boton['imagen'], boton['rect'])
            textBoton = boton['texto1']
        for i in range(len(textBoton)):
            texto=textBoton[i]
            textLabel = textFont_botones.render(texto, True, NEGRO)
            lcd.blit(textLabel, (scrn_width - tam_boton - 30,boton['rect'][1]-18 + (i*displayPixelWidth/3))  )
    dibujarBarraColor(map_width)

def cerrarTodo():
    global confiCal, configurar, grabarVideo, salirGrabacionCSV, salir
    confiCal = configurar = grabarVideo = False
    salirGrabacionCSV = salir = True

def connection():
    global MINTEMP, MAXTEMP, fileNameLimits, raiz, configurar, salirMainScrn, botones, botonesConfig, salirGrabacionCSV, grabandoCSV, ip, servidorThread, newCommand, s, c, servidor, extActual, extActual2, videoCon, grabarVideo, grabandoVideo, archivoDatosNuevo, archivoVideoNuevo
    #host = socket.gethostname()
    #ip = socket.gethostbyname(host)
    clientDisconnect = False
    if servidor:
        #ip = get('https://api.ipify.org').text
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s = socket.socket()
        try:
            port = 8081
            s.bind(('', port))
            s.listen(1)
            c, address = s.accept()
            c.send(str.encode('Conectado a ' + ip))
            while not salir:
                servidorThread = True
                nuevaRaiz = True
                nuevoArchivo = True
                understood = False
                global newCommand
                #ready = select.select([s], [], [], 1)
                #if ready[0]:
                newCommand = (c.recv(1024))
                if newCommand == 'PNG':
                    extActual = 'PNG'
                    understood = True
                elif newCommand == 'CSV':
                    extActual = 'CSV'
                    understood = True
                elif newCommand == 'TXT':
                    extActual = 'TXT'   
                    understood = True
                elif newCommand == 'MP4':
                    extActual2 = 'MP4'
                    understood = True
                elif newCommand == 'MKV':
                    extActual2 = 'MKV'
                    understood = True
                elif newCommand == 'MAP':
                    videoCon = 'MAP'
                    understood = True
                elif newCommand == 'FULLSCREEN':
                    videoCon = 'FULLSCREEN'
                    understood = True
                elif newCommand == 'I_VIDEO':
                    configurar = salirMainScrn = botones[2]['selected'] = botonesConfig[2]['selected'] = False
                    sleep(1)
                    grabarVideo = True
                    understood = True
                elif newCommand == 'D_VIDEO':
                    grabarVideo = False
                    grabandoVideo = True
                    understood = True
                elif newCommand == 'I_DATOS':
                    configurar = salirMainScrn = botones[2]['selected'] = botonesConfig[2]['selected'] = False
                    sleep(1)
                    salirGrabacionCSV = grabandoCSV = False
                    understood = True
                elif newCommand == 'D_DATOS':
                    salirGrabacionCSV = grabandoCSV = True
                    understood = True
                elif newCommand == 'TEMP':
                    botones[3]['selected'] = False
                    understood = True
                elif newCommand == 'VALUES':
                    botones[3]['selected'] = True
                    understood = True
                elif newCommand == 'ROOT':
                    while nuevaRaiz:
                        c.send(str.encode('\n\rRaiz es: ' + raiz +'\n\rDesea cambiarla? (SI/NO)'))
                        newCommand = (c.recv(1024))
                        if newCommand == 'SI':
                            raizInfo = ('Ingrese nueva raiz: \n\r\n\rCarpetas: ')
                            for name in os.listdir(raiz):
                                if os.path.isdir(os.path.join(raiz, name)):
                                    raizInfo = raizInfo + ('\n\r'+ name)
                            c.send(str.encode(raizInfo + '\n\r".." para regresar\n\r'))
                            newCommand = c.recv(1024)
                            if newCommand == '..':
                                raizInfo = raiz.split('/', -2)
                                raizInfo2 = ''
                                for b in range(0, len(raizInfo)-2):
                                    raizInfo2 = raizInfo2 + raizInfo[b] + '/'
                                raiz = raizInfo2
                            else:
                                raiz = (raiz + newCommand + '/')
                        elif newCommand == 'NO':
                            nuevaRaiz = False
                    understood = True
                elif newCommand == 'EXPORT':
                    while nuevoArchivo:
                        archivoInfo = '\n\rRaiz es: ' + raiz +'\n\rArchivos exportables en carpeta:'
                        for name in os.listdir(raiz):
                            if name.endswith('.txt') or name.endswith('.csv') or name.endswith('.png') or name.endswith('.mp4') or name.endswith('.mkv'):
                                    archivoInfo = archivoInfo + ('\n\r'+ name)
                        archivoInfo = archivoInfo + '\n\n\rPara modificar carpeta usar ROOT\n\rDesea exportar algun archivo? (SI/NO)'
                        c.send(str.encode(archivoInfo))
                        newCommand = (c.recv(1024))
                        if newCommand == 'SI':
                            archivoInfo = ('\n\rPara archivos TXT, CSV, PNG use D_EXPORT\n\rPara archivos MP4, MKV use V_EXPORT\n\n\rIngrese archivo a exportar:')
                            c.send(str.encode(archivoInfo))
                            newCommand = c.recv(1024)
                            archivoActual = (raiz + newCommand)
                            if archivoActual.endswith('.txt') or archivoActual.endswith('.csv') or archivoActual.endswith('.png'):
                                extActual = newCommand[-3:].upper()
                                archivoDatosNuevo = archivoActual
                            elif archivoActual.endswith('.mp4') or archivoActual.endswith('.mkv'):
                                extActual2 = newCommand[-3:].upper()
                                archivoVideoNuevo = archivoActual
                            nuevoArchivo = False
                        elif newCommand == 'NO':
                            nuevoArchivo = False
                    understood = True
                elif newCommand == 'V_EXPORT':
                    archivo = open(archivoVideoNuevo, 'rb')
                    sleep(10)
                    c.send(str.encode(extActual2))
                    sleep(10)
                    buff = archivo.read(1024)
                    while(buff):
                        c.send(buff)
                        buff = archivo.read(1024) 
                    c.send(str.encode('Done'))
                    sleep(10)
                    understood = True
                elif newCommand == 'D_EXPORT':
                    archivo = open(archivoDatosNuevo, 'rb')
                    sleep(10)
                    c.send(str.encode(extActual))
                    sleep(10)
                    buff = archivo.read(1024)
                    while(buff):
                        c.send(buff)
                        buff = archivo.read(1024) 
                    c.send(str.encode('Done'))
                    sleep(10)
                    understood = True
                elif newCommand.startswith('MINTEMP'):
                    MINTEMP = int(newCommand[7:])
                    guardarVariables(MINTEMP, MAXTEMP, fileNameLimits)
                    understood = True
                elif newCommand.startswith('MAXTEMP'):
                    MAXTEMP = int(newCommand[7:])
                    guardarVariables(MINTEMP, MAXTEMP, fileNameLimits)
                    understood = True
                elif newCommand.startswith('SERIAL'):
                    serialTemp = str(newCommand[6:])
                    serialTemp = bytes(serialTemp+'\n')
                    input_box1.ser.write(serialTemp)
                    print(input_box1.ser.readline().decode('utf-8').rstrip())
                    understood = True
                elif newCommand == 'C_EXIT':
                    sleep(5)
                    clientDisconnect = True
                    understood = True
                elif newCommand == 'S_EXIT':
                    servidor = False
                    ip = 'N/A'
                    understood = True
                if not (newCommand == 'D_EXPORT') or not (newCommand == 'V_EXPORT'):
                    if understood:
                        c.send(str.encode('Recibido'))
                    else:
                        c.send(str.encode('Revisar comando'))
                if clientDisconnect:
                    c.close()
                    clientDisconnect = False
                    c, address = s.accept()
                    c.send(str.encode('Conectado a ' + ip))
                if not servidor:
                    s.close()
                    break
            c.close()
            s.close()
        except Exception as e:
            print(e)
            s.close()

def interfaz():
    global newCommand, ip, salir, map_height, map_width, displayPixelWidth, displayPixelHeight, lcd, botones, salirGrabacionCSV, grabarVideo, configurar, confiCal, box_active, promedioTem, confiMax
    text = "0"
    clock = pygame.time.Clock()
    while not salir:
        if confiMax:
            for event in pygame.event.get():
                input_box1.handle_event(event)
            input_box1.update()
            input_box1.draw(lcd)
            pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cerrarTodo()
                quit()
            if event.type == MOUSEBUTTONUP:
                mouse = event.pos
                if input_box.collidepoint(event.pos) and not tomaHabilitada:
                    # Toggle the active variable.
                    box_active = True
                else:
                    box_active = False
                # Change the current color of the input box.
                presionarPantalla(mouse)
            text = "0" if tomaHabilitada else text
            if event.type == pygame.KEYDOWN:
                # Permite terminar el programa
                if event.key == pygame.K_q:
                    cerrarTodo()
                # Alterna entre 'pantalla completa' y 'ventana'.
                elif event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()
                elif not tomaHabilitada and box_active:
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        if not re.match(r'^-?\d+(?:\.\d+)?$', event.unicode) is None or event.unicode == ".":
                            text += event.unicode
                    try:
                        text = "0" if text == "" else text
                        print(text)
                        promedioTem = float(text)
                    except Exception as e:
                        print(e)
        pygame.time.wait(5)

def botonesPantallaConfiguracion():
    global terminar, s, ip, servidorThread, servidor, videoCon, extActual, extActual2, root, raiz, salirGrabacionCSV, grabarVideo, botones, configurar, salirMainScrn, confiMax, MAXTEMP, MINTEMP, confiMin, salir, confiCal, c
    if botonesConfig[0]['selected']:
        confiMax = True
    elif botonesConfig[1]['selected']:
        confiCal = True
    elif botonesConfig[2]['selected']:
        configurar = salirMainScrn = botones[2]['selected'] = botonesConfig[2]['selected'] = False
    elif botonesConfig[3]['selected']:
        confiMin = True
    elif botonesConfig[4]['selected']:
        grabarVideo = False
        salirGrabacionCSV = True
        pygame.time.wait(20)
        try:
            root = Tkinter.Tk()
            root.title('Si cierran esto, el programa se muere LOLZ')
            root.geometry('500x1')
            root.wm_state('iconic')
            root.protocol('WM_DELETE_WINDOW', preventClosing)
            root.directory = tkFileDialog.askdirectory()
            raiz = root.directory + "/"
            root.destroy()
        except Exception as e:
            print(e)
            root.destroy()
    elif botonesConfig[5]['selected']:
        extActual = 'TXT'
    elif botonesConfig[6]['selected']:
        extActual = 'CSV'
    elif botonesConfig[7]['selected']:
        extActual2 = 'MKV'
    elif botonesConfig[8]['selected']:
        extActual2 = 'MP4'
    elif botonesConfig[9]['selected']:
        videoCon = 'MAP'
    elif botonesConfig[10]['selected']:
        videoCon = 'FULLSCREEN'
    elif botonesConfig[11]['selected']:
        extActual = 'PNG'
    elif botonesConfig[13]['selected']:
        if not servidor:
            servidor = True
            print('servidor inicializado')
            threading.Thread(target=connection).start()
        else:
            if servidorThread:
                servidor = False
                print('servidor apagado')
                ip = 'N/A'
                try:
                    c.send(str.encode('Servidor desconectado'))
                    c.close()
                    s.close()
                except Exception as e:
                    print(e)
                    c.close()
                    s.close()
    for boton in range(0,12):
        botonesConfig[boton]['selected'] = False
    botonesConfig[12]['selected'] = servidor

def preventClosing():
    pass

def botonesConfiMax():
    global salirGrabacionCSV, grabarVideo, botones, configurar, salirMainScrn, confiMax, MAXTEMP, MINTEMP, confiMin, salir, confiCal
    if botonesMaximo[0]['selected']:
        MAXTEMP = constrain(MAXTEMP + 1, MINTEMP + 1, 100)
    elif botonesMaximo[1]['selected']:
        MAXTEMP = constrain(MAXTEMP - 1, MINTEMP + 1, 100)
    elif botonesMaximo[2]['selected']:
        guardarVariables(MINTEMP, MAXTEMP, fileNameLimits)
        confiMax = False
    for boton in botonesMaximo:
        boton['selected'] = False

def botonesConfiMin():
    global salirGrabacionCSV, grabarVideo, botones, configurar, salirMainScrn, confiMax, MAXTEMP, MINTEMP, confiMin, salir, confiCal
    if botonesMaximo[0]['selected']:
        MAXTEMP = constrain(MAXTEMP + 1, MINTEMP + 1, 100)
    elif botonesMaximo[1]['selected']:
        MAXTEMP = constrain(MAXTEMP - 1, MINTEMP + 1, 100)
    elif botonesMaximo[2]['selected']:
        guardarVariables(MINTEMP, MAXTEMP, fileNameLimits)
        confiMin = False
    elif botonesMaximo[3]['selected']:
        MINTEMP = constrain(MINTEMP + 1, 0, MAXTEMP - 1)
    elif botonesMaximo[4]['selected']:
        MINTEMP = constrain(MINTEMP - 1, 0, MAXTEMP - 1)
    # dibujar_botones_rango("Tope temperatura maxima", MAXTEMP)
    for boton in botonesMaximo:
        boton['selected'] = False

def botonesConfiCal():
    global salirGrabacionCSV, grabarVideo, botones, configurar, salirMainScrn, confiMax, MAXTEMP, MINTEMP, confiMin, salir, confiCal, promedioTem, tomaHabilitada, xParameter, bParameter, calY, calX
    if botonesCalibracion[0]['selected']:
        xParameter, bParameter = regLineal(calX, calY)
        guardarVariables(xParameter, bParameter, fileNameCalibration)
    elif botonesCalibracion[1]['selected']:
        calX = []
        calY = []
        confiCal = False
    elif botonesCalibracion[2]['selected']:
        promedioTem -= 0.1
    elif botonesCalibracion[3]['selected']:
        promedioTem += 0.1
    elif botonesCalibracion[4]['selected']:
        if not tomaHabilitada:
            calX.append(int(promedioDatos))
            calY.append(promedioTem)
        tomaHabilitada ^= 1
        for bot in range(2,6):
            botonesCalibracion[bot]['habilitado'] ^= 1
        if len(calX) >= 2:
            botonesCalibracion[0]['habilitado'] = True
    elif botonesCalibracion[5]['selected']:
        tomaHabilitada ^= 1
        for bot in range(2,6):
            botonesCalibracion[bot]['habilitado'] ^= 1
    for boton in botonesCalibracion:
        boton['selected'] = False

def presionarPantalla(mouse):
    global salirGrabacionCSV, grabarVideo, botones, configurar, salirMainScrn, confiMax, MAXTEMP, MINTEMP, confiMin, salir, confiCal, click
    scrnConfi = confiMax or confiMin or confiCal
    if corriendoMainScrn:
        for boton in botones:
            boton['selected'] = boton['selected'] ^ boton['rect'].colliderect([mouse[0]-1, mouse[1], 1, 1])
        salirGrabacionCSV = not botones[1]['selected']
        grabarVideo = botones[0]['selected']
        configurar = botones[2]['selected']
        if not configurar:
            dibujar_botones_iniciales(botones)
    elif configurando and not scrnConfi:
        for boton in botonesConfig:
            boton['selected'] = boton['rect'].colliderect([mouse[0] - 1, mouse[1], 1, 1])
        botonesPantallaConfiguracion()
    elif confiMax:
        for boton in botonesMaximo:
            boton['selected'] = boton['rect'].colliderect([mouse[0] - 1, mouse[1], 1, 1])
        botonesConfiMax()
    elif confiMin:
        for boton in botonesMaximo:
            boton['selected'] = boton['rect'].colliderect([mouse[0] - 1, mouse[1], 1, 1])
        botonesConfiMin()
    elif confiCal:
        for boton in botonesCalibracion:
            boton['selected'] = boton['rect'].colliderect([mouse[0] - 1, mouse[1], 1, 1]) and boton['habilitado']
        botonesCalibracion[4]['selected'] = botonesCalibracion[4]['rect'].colliderect([mouse[0] - 1, mouse[1], 1, 1])
        botonesConfiCal()
    click = True

def mainSrcn():
    global corriendoMainScrn, csv_pixels
    corriendoMainScrn = True
    dibujar_botones_iniciales(botones)
    while not salirMainScrn:
        #read the pixels
        try:
            pixelsMap = sensor.readPixels()
            # pixelsMap = np.random.rand(64,1)*100
            pixels = [map(p, MINTEMP, MAXTEMP, 0, COLORDEPTH - 1) for p in pixelsMap]
            if botones[3]['selected']:
                for ix in range(8):
                    for jx in range(8):
                        pygame.draw.rect(lcd, colors[constrain(int(pixels[ix * 8 + jx]), 0, COLORDEPTH - 1)], (displayPixelHeight * ix, displayPixelWidth * jx, displayPixelHeight, displayPixelWidth))
                        textTemp = textFont.render(str(round((pixelsMap[ix * 8 + jx] / 0.25) * xParameter +bParameter, 2)), True, (255, 255, 255))
                        textTempRec = textTemp.get_rect()
                        textTempRec.center = ( int( displayPixelHeight * (ix+0.5) ) , int( displayPixelWidth * (jx + 0.5) ))
                        lcd.blit(textTemp, textTempRec)
            else:
                # perdorm interpolation
                bicubic = griddata(points, pixels, (grid_x, grid_y), method='cubic')

                # draw everything
                for ix, row in enumerate(bicubic):
                    for jx, pixel in enumerate(row):
                        pygame.draw.rect(lcd, colors[constrain(int(pixel), 0, COLORDEPTH - 1)], (7.5 * ix, 7.5 * jx, displayPixelHeightCubic, displayPixelWidthCubic))
            if grabandoCSV:
                tiempo_actual_csv = time() -tiempo_inicio_csv
                pixelsMap.insert(0,tiempo_actual_csv)
                csv_pixels.append(pixelsMap)

            if not salirMainScrn:
                pygame.display.update()
        except Exception as e:
            print(e)
    corriendoMainScrn = False

x_file_csv = 0
def grabar_csv():
    global salirGrabacionCSV, botones, extActual, grabandoCSV, x_file_csv,tiempo_inicio_csv, csv_pixels, archivoDatosNuevo
    grabandoCSV = True
    dir = listdir(raiz)
    if not "dataFiles" in dir:
        try:
            os.system("mkdir " +raiz+ "dataFiles")
        except Exception as e:
            print(e)
    filename = raiz +"dataFiles/camara_termica." + extActual.lower()
    if not raiz + "dataFiles/camara_termica" + str(x_file_csv) + "." + extActual.lower() in glob.glob(raiz +"dataFiles/*." + extActual.lower()):
        filename =raiz + "dataFiles/camara_termica" + str(x_file_csv) + "." + extActual.lower()
    else:
        x_file_csv += 1
        grabar_csv()
    tiempo_inicio_csv = time()
    archivoDatosNuevo = filename
    if extActual == 'PNG':
        rect = pygame.Rect(0, 0, 480, 480)
        sub = lcd.subsurface(rect)
        pygame.image.save(sub, filename)
        salirGrabacionCSV = True
    else:
        #salirGrabacionCSV = False
        archivo = open(filename, "w")
        csv_escritor = csv.writer(archivo)
            #Encabezado del archivo
        text_header = ["Tiempo"]
        for i in range(nPixels):
            text_header.append("Pixel "+ str(i))
        csv_escritor.writerow(text_header)
        archivo.flush()
        archivo.close()
        while not salirGrabacionCSV:
            archivo = open(filename, "a")
            csv_escritor = csv.writer(archivo)
            for i in range(len(csv_pixels)):
                csv_escritor.writerow(csv_pixels[i])
            csv_pixels = []
            archivo.flush()
            archivo.close()
            pygame.time.wait(1000)
    csv_pixels = []
    grabandoCSV = False

x_file_video = 0
def iniciarGrabarVideo():
    print('video Iniciado')
    global videoCon, lcd, p, grabandoVideo, x_file_video, archivoVideoNuevo
    grabandoVideo = True
    filename = raiz + "videoFiles/camara_termica" + str(x_file_video) + "." + extActual2.lower()
    dir = listdir(raiz)
    if not "videoFiles" in dir:
        try:
            os.system("mkdir " +raiz+ "videoFiles")
        except Exception as e:
            print(e)
    if not raiz +"videoFiles/camara_termica" + str(x_file_video) + "." + str(extActual2.lower()) in glob.glob(raiz +"videoFiles/*." + extActual2.lower()):
        filename = raiz +"videoFiles/camara_termica" + str(x_file_video) + "." + extActual2.lower()
    else:
        x_file_video += 1
        iniciarGrabarVideo() 
    archivoVideoNuevo = filename
    if videoCon == 'MAP':
        comando = 'ffmpeg -video_size 480x480 -framerate 30 -f x11grab -i :0.0+0,30 -crf 0 -preset:v ultrafast -af aresample=async=1:first_pts=0 ' + filename
    elif videoCon == 'FULLSCREEN':
        comando = "ffmpeg -framerate 30 -f alsa -r 10 -f x11grab -s $(xdpyinfo | grep dimensions | awk '{print $2;}') -i ${DISPLAY} -c:v libx264rgb -crf 0 -preset:v ultrafast -af aresample=async=1:first_pts=0 "+ filename
    p = subprocess.Popen(comando, shell=True, stdin=None, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, close_fds=True)
    
def detenerVideo():
    print('video detenido')
    global p, grabandoVideo
    os.killpg(os.getpgid(p.pid), signal.SIGINT)
    grabandoVideo = False

def configuracionPantalla():
    global salirMainScrn, configurando, click, lcd, input_box1, clock
    configurando = True
    salirMainScrn = True
    while configurar:
        #if click:
            lcd.fill(BLANCO)
            if confiMax:
                dibujar_botones_rango('save', MAXTEMP)
                textLabel = textFont_temp.render("Comunicacion serial con Arduino:", True, NEGRO)
                lcd.blit(textLabel, (190, 20))
                textLabel = textFont_temp.render(input_box1.line, True, NEGRO)
                lcd.blit(textLabel, (30, 170))
                input_box1.update()
                input_box1.draw(lcd)
                pygame.display.update()
            elif confiMin:
                dibujar_botones_rango('todos', MINTEMP)
            elif confiCal:
                dibujar_botones_calibracion()
                dibujarBarraColor(map_width - 10)
                pygame.time.wait(20)
            else:
                dibujar_botones_configuracion()
            if not confiCal:
                pygame.display.update()
            pygame.time.wait(5)
            click = False
    configurando = False
    
########################################################################MODIFICAR calibracion
########################################################################AUTOMATICA

def confiCalibracion():
    global configurandoCal, configurar, promedioTem, promedioDatos
    configurandoCal = True
    pygame.display.update()
    pixelsMap = []
    while confiCal:
        try:
            if tomaHabilitada:
                pixelsMap = sensor.readPixels()
                # pixelsMap = np.random.rand(64, 1) * 100
            pixels = [map(p, MINTEMP, MAXTEMP, 0, COLORDEPTH - 1) for p in pixelsMap]
            promTem = 0
            promDatos = 0

            for ix in range(3,5):
                for jx in range(3,5):
                    pygame.draw.rect(lcd, colors[constrain(int(pixels[ix * 8 + jx]), 0, COLORDEPTH - 1)], (displayPixelHeight * ix, displayPixelWidth * jx, displayPixelHeight, displayPixelWidth))
                    promTem +=round((pixelsMap[ix * 8 + jx] / 0.25) * xParameter +bParameter, 2)
                    promDatos += pixelsMap[ix * 8 + jx] / 0.25
            if tomaHabilitada:
                promedioTem = promTem / 4
                promedioDatos = promDatos / 4
            actualizarTemCal(promedioTem)
            if confiCal:
                pygame.display.update()
        except Exception as e:
            print(e)
    configurandoCal = False

def principal():
    global a, salirMainScrn, salirGrabacionCSV, s
    while not salir:
        if not salirMainScrn and not corriendoMainScrn:
            threading.Thread(target=mainSrcn).start()
        if not salirGrabacionCSV and not grabandoCSV:
            a = threading.Thread(target=grabar_csv).start()
        if grabarVideo and not grabandoVideo:
            iniciarGrabarVideo()
        elif not grabarVideo and grabandoVideo:
            detenerVideo()
        if configurar and not configurando:
            threading.Thread(target=configuracionPantalla).start()
        if confiCal and not configurandoCal:
            threading.Thread(target=confiCalibracion).start()
        pygame.time.wait(50)
    salirMainScrn = True
    salirGrabacionCSV = True

threading.Thread(target=interfaz).start()
threading.Thread(target=principal).start()





