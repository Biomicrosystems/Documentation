import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import time   
from tkinter import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)   
import cv2
import numpy as np
from tkinter import ttk


vid = cv2.VideoCapture(0)

bins = 8

fig, ax = plt.subplots()
ax.set_title('Histogram (RGB)')
ax.set_xlabel('Bin')
ax.set_ylabel('Frequency')
ax.set_xlim(0, bins-1)
ax.set_ylim(0, 1)

prev_frame_time = 0
new_frame_time = 0

lw = 3
alpha = 0.9

lineR, = ax.plot(np.arange(bins), np.zeros((bins,)), c='r', lw=lw, alpha=alpha, label='Red')
lineG, = ax.plot(np.arange(bins), np.zeros((bins,)), c='g', lw=lw, alpha=alpha, label='Green')
lineB, = ax.plot(np.arange(bins), np.zeros((bins,)), c='b', lw=lw, alpha=alpha, label='Blue')

ax.legend()
plt.grid()

def animate(i):
    global prev_frame_time, new_frame_time
    ret, frame = vid.read()
    #cv2.imshow('frame', frame)
    numPixels = np.prod(frame.shape[:2])
    (b, g, r) = cv2.split(frame)
    
    histogramR = cv2.calcHist([r], [0], None, [bins], [0, 255])/ numPixels
    histogramG = cv2.calcHist([g], [0], None, [bins], [0, 255])/ numPixels
    histogramB = cv2.calcHist([b], [0], None, [bins], [0, 255])/ numPixels


    lineR.set_ydata(histogramR)
    lineG.set_ydata(histogramG)
    lineB.set_ydata(histogramB)
    
    new_frame_time = time.time()
 
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time
 

    fps = int(fps)
    str_fps = str(fps)
    frame_w_fps = frame
    cv2.putText(frame_w_fps,str_fps,(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0, 255, 0),2)
    cv2.imshow('frame', frame_w_fps)
     
    return lineR, lineG, lineB

def iniciar():
    global anim, vid
    num_input = return_videoinput()
    vid = cv2.VideoCapture(num_input)
    anim = animation.FuncAnimation(fig, animate, 
                               frames=None, interval=10, blit=True)
    canvas.draw()
    
def cerrar():
    root.destroy()
    sys.exit(0)

def return_videoinput():
    return int(Combobox_Entrada.get())

root = Tk()#Ventana principal
root.title('Histograma')
root.resizable(False, False)

canvas = FigureCanvasTkAgg(fig, master = root)
canvas.get_tk_widget().grid(column=0,row=0)

btnIniciar = Button(root,text='Iniciar',command=iniciar)
btnIniciar.grid(column=0,row=2)

button4_opw  = Button(root, text = "Cerrar", command = cerrar )
button4_opw.grid(column=0,row=3)

Combobox_Entrada = ttk.Combobox(root,state="readonly",values=["0","1","2","3"])
Combobox_Entrada.set("0")
Combobox_Entrada.grid(column=0,row=5)

toolbarFrame = Frame(master = root)
toolbarFrame.grid(column=0,row=1)
toolbar = NavigationToolbar2Tk(canvas,toolbarFrame)



root.mainloop()