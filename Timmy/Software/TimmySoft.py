from tkinter import *

from tkinter import ttk

import cv2

import numpy as np

from PIL import Image, ImageTk


#Entrada de video
num_input = 0

frame = []

#Variables Calibración
punto_inicial_cal = []
punto_final_cal = []
distancia_pixels_cal = []
cte_calibracion = []
dist_conocida_cal = []
calibrando = False

#Variables Medición
punto_inicial_med = []
punto_final_med = []
cte_calibracion_med = []
distancia_pixels_med = []
distancia_mm = []
midiendo = False
str_cte_calibracion = ''

#Exportar imágenes
img_counter = 0

#Calibración global
cte_calibracion_global = 0

#FUNCION DE VISUALIZACION NORMAL Y PREPROCESAMIENTO (RGB, ALPHA Y BETA)-----------------------------------------------------------------------------------------------
def visualizar_normal():
    global cap,frame
    ret, frame = cap.read()
    if ret == True:
        red_s = slider_r.get()
        green_s = slider_g.get()
        blue_s = slider_b.get()
        contraste_s = slider_contraste.get()
        brillo_s = slider_brillo.get()

        (b, g, r) = cv2.split(frame)  
        b = cv2.add(b,blue_s)
        g = cv2.add(g,green_s)
        r = cv2.add(r,red_s)
        merged = cv2.merge([b,g,r])

        merged_ajusted = cv2.convertScaleAbs(merged, alpha=contraste_s, beta=brillo_s)

        frame = cv2.cvtColor(merged_ajusted, cv2.COLOR_BGR2RGB)
        
        escala_deseada = txtEntryScale.get()
             
        if cte_calibracion_global != 0 and escala_deseada != '':
            escala_pix = float(escala_deseada)*10**3*1/float(cte_calibracion_global)+40
            escala_pix_int = int(escala_pix)
            cv2.line(frame,(40,420),(40,440),(0, 255, 0), 2)
            cv2.line(frame,(40,430),(escala_pix_int,430),(0, 255, 0), 2)
            cv2.line(frame,(escala_pix_int,420),(escala_pix_int,440),(0, 255, 0), 2)
            msg = escala_deseada + ' mm'
            cv2.putText(frame,msg,(50,415),cv2.FONT_HERSHEY_COMPLEX,0.7,(0, 255, 0),2)
        
        im = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=im)
        lblVideo.configure(image=img)
        lblVideo.image = img
        lblVideo.after(10, visualizar_normal)



#CALIBRACIÓN-----------------------------------------------------------------------------------------------------------------------------------
def visualizar_calibracion():
    global cap,frame
    ret, frame = cap.read()
    if ret == True:
        cv2.putText(frame,'Calibrando',(10,30),cv2.FONT_HERSHEY_COMPLEX,0.7,(0, 255, 0),2)
        if len(punto_final_cal) != 0  and len(punto_inicial_cal) != 0:
            cv2.arrowedLine(frame, punto_inicial_cal, punto_final_cal, (0, 255, 0), 2)
            cv2.arrowedLine(frame, punto_final_cal, punto_inicial_cal, (0, 255, 0), 2)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=im)
        lblVideo.configure(image=img)
        lblVideo.image = img
        lblVideo.after(10, visualizar_calibracion)
        calcularctecalibracion()

def pressed1(event):  
    global punto_inicial_cal, dist_conocida_cal, cte_calibracion_med,punto_inicial_med, calibrando, midiendo
    punto_inicial_cal = (event.x, event.y)
    punto_inicial_med = (event.x, event.y)
    if calibrando == True:
        dist_conocida_cal = float(txtEntryDistCal.get())



def released1(event):
    global punto_final_cal, punto_final_med, midiendo
    punto_final_cal = (event.x, event.y)
    punto_final_med = (event.x, event.y)

    
def calcularctecalibracion():
    global distancia_pixels_cal, punto_inicial_cal, punto_final_cal, str_cte_calibracion, cte_calibracion_global
    if len(punto_final_cal) != 0  and len(punto_inicial_cal) != 0:
        distancia_pixels_cal = np.sqrt((punto_inicial_cal[0]-punto_final_cal[0])**2 + (punto_inicial_cal[1]-punto_final_cal[1])**2)
        cte_calibracion = dist_conocida_cal*10**3/distancia_pixels_cal #um/pixel
        str_cte_calibracion = format(cte_calibracion,'.5f')
        lblCteCal_val.config(text=str_cte_calibracion)
        cte_calibracion_global = cte_calibracion



#MEDICIÓN-----------------------------------------------------------------------------------------------------------------------------------
def visualizar_medicion():
    global cap,frame
    ret, frame = cap.read()
    if ret == True:
        if cte_calibracion_global != 0:
             max_scale_float = 560*float(cte_calibracion_global)*10**-3 #Valor máximo para una buena visualización 560
             max_scale_str = format(max_scale_float,'.5f')
             lblScaleMaxVal.config(text=max_scale_str)
        
        escala_deseada = txtEntryScale.get()
             
        if cte_calibracion_global != 0 and escala_deseada != '':
            escala_pix = float(escala_deseada)*10**3*1/float(cte_calibracion_global)+40
            escala_pix_int = int(escala_pix)
            cv2.line(frame,(40,420),(40,440),(0, 255, 0), 2)
            cv2.line(frame,(40,430),(escala_pix_int,430),(0, 255, 0), 2)
            cv2.line(frame,(escala_pix_int,420),(escala_pix_int,440),(0, 255, 0), 2)
            msg = escala_deseada + ' mm'
            cv2.putText(frame,msg,(50,415),cv2.FONT_HERSHEY_COMPLEX,0.7,(0, 255, 0),2)
            

        cv2.putText(frame,'Midiendo',(10,30),cv2.FONT_HERSHEY_COMPLEX,0.7,(0, 255, 0),2)


        if len(punto_final_med) != 0  and len(punto_inicial_med) != 0:
            cv2.arrowedLine(frame, punto_inicial_med, punto_final_med, (0, 255, 0), 2)
            cv2.arrowedLine(frame, punto_final_med, punto_inicial_med, (0, 255, 0), 2)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        lblCteCalMed_val.config(text=str_cte_calibracion)
        
        im = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=im)
        lblVideo.configure(image=img)
        lblVideo.image = img
        lblVideo.after(10, visualizar_medicion)
        calcularmedida()
    
def calcularmedida():
    global distancia_pixels_med
    if len(punto_final_med) != 0  and len(punto_inicial_med) != 0:
        distancia_pixels_med = np.sqrt((punto_inicial_med[0]-punto_final_med[0])**2 + (punto_inicial_med[1]-punto_final_med[1])**2)
        distancia_mm = distancia_pixels_med*cte_calibracion_global*10**-3
        str_distancia_mm = format(distancia_mm,'.5f')
        lblDistMed_val.config(text=str_distancia_mm)



#CANNY (CONTORNOS)-----------------------------------------------------------------------------------------------------------
def visualizar_canny():
    global cap,frame
    ret, frame = cap.read()
    if ret == True:
        ths1 = slider_th1.get()
        ths2 = slider_th2.get()
        frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        frame = cv2.Canny(frame_gray,ths1,ths2)
        
        escala_deseada = txtEntryScale.get()
             
        if cte_calibracion_global != 0 and escala_deseada != '':
            escala_pix = float(escala_deseada)*10**3*1/float(cte_calibracion_global)+40
            escala_pix_int = int(escala_pix)
            
            cv2.line(frame,(40,420),(40,440),(255, 255, 255), 2)
            cv2.line(frame,(40,430),(escala_pix_int,430),(255, 255, 255), 2)
            cv2.line(frame,(escala_pix_int,420),(escala_pix_int,440),(255, 255, 255), 2)
            msg = escala_deseada + ' mm'
            cv2.putText(frame,msg,(50,415),cv2.FONT_HERSHEY_COMPLEX,0.7,(255, 255, 255),2)
        
        im = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=im)
        lblVideo.configure(image=img)
        lblVideo.image = img
        lblVideo.after(10, visualizar_canny)


#LIMPIAR------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def limpiar():
    cap.release()
    lblVideo.image = ""
    rad1.configure(state='active')
    rad2.configure(state='active')
    rad3.configure(state='active')
    rad4.configure(state='active')
    
    if selection.get() == 1:
        slider_r.grid_forget()
        slider_g.grid_forget()
        slider_b.grid_forget()
        slider_brillo.grid_forget()
        slider_contraste.grid_forget()
        btnLimpiar.grid_forget()
        btnCapturar.grid_forget()
        selection.set(0)
    
    if selection.get() == 2:
        lblDistCalibrar.grid_forget()
        txtEntryDistCal.grid_forget()
        lblCteCal.grid_forget()
        lblCteCal_val.grid_forget()
        btnLimpiar.grid_forget()
        btnCapturar.grid_forget()
        selection.set(0)
    
    if selection.get() == 3:       
        lblCteCalMed.grid_forget()
        lblCteCalMed_val.grid_forget()
        lblDistMed.grid_forget()
        lblDistMed_val.grid_forget()
        btnLimpiar.grid_forget()
        lblScaleMax.grid_forget()
        lblScaleMaxVal.grid_forget()
        lblScale.grid_forget()
        txtEntryScale.grid_forget()
        btnCapturar.grid_forget()
        selection.set(0)
        
    if selection.get() == 4:
        slider_th1.grid_forget()
        slider_th2.grid_forget()
        btnLimpiar.grid_forget()
        btnCapturar.grid_forget()
        selection.set(0)
                
#CAPTURAS---------------------------------------------------------------------------------------------------------------------------------           
def capturar():
    global img_counter, frame
    img_name = "img_frame_{}.png".format(img_counter)
    if selection.get() == 1 or selection.get() == 2 or selection.get() == 3:
        frame_img = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    else:
        frame_img = frame
    cv2.imwrite(img_name,frame_img)
    print('Imagen exportada')
    img_counter+=1
    
#QUÉ FUNCION SE SELECIONÓ NORMAL, CALIBRACIÓN O MEDICIÓN------------------------------------------------------------------------------------------------------------------------
def que_se_selecciono():
    global cap, midiendo, calibrando, punto_inicial_cal, punto_final_cal, punto_inicial_med, punto_final_med, num_input
    if selection.get() == 1: #NORMAL
        rad2.configure(state='disabled')
        rad3.configure(state='disabled')
        rad4.configure(state='disabled')
        slider_r.grid(column=0,row=2)
        slider_g.grid(column=0,row=3)
        slider_b.grid(column=0,row=4)
        slider_contraste.grid(column=1,row=2)
        slider_brillo.grid(column=1,row=3)
        btnLimpiar.grid(column=1,row=4)
        btnCapturar.grid(column=2,row=2)
        num_input = return_videoinput()
        cap = cv2.VideoCapture(num_input)
        visualizar_normal()
    if selection.get() == 2: #CALIBRACIÓN
        punto_inicial_cal = []
        punto_final_cal = []
        rad1.configure(state='disabled')
        rad3.configure(state='disabled')
        rad4.configure(state='disabled')
        num_input = return_videoinput()
        cap = cv2.VideoCapture(num_input)
        lblDistCalibrar.grid(column=0,row=2)
        txtEntryDistCal.grid(column=1,row=2)
        lblCteCal.grid(column=0,row=3)
        lblCteCal_val.grid(column=1,row=3)
        btnLimpiar.grid(column=2,row=2)
        btnCapturar.grid(column=2,row=3)
        calibrando = True
        midiendo = False
        visualizar_calibracion()    
    if selection.get() == 3: #MEDICIÓN
        punto_inicial_med = []
        punto_final_med = []
        rad1.configure(state='disabled')
        rad2.configure(state='disabled')
        rad4.configure(state='disabled')
        num_input = return_videoinput()
        cap = cv2.VideoCapture(num_input)
        lblCteCalMed.grid(column=0,row=2)
        lblCteCalMed_val.grid(column=1,row=2)
        lblDistMed.grid(column=0,row=3)
        lblDistMed_val.grid(column=1,row=3)
        btnLimpiar.grid(column=2,row=2)
        lblScaleMax.grid(column=0,row=4)
        lblScaleMaxVal.grid(column=1,row=4)
        lblScale.grid(column=0,row=5)
        txtEntryScale.grid(column=1,row=5)
        btnCapturar.grid(column=2,row=3)
        midiendo = True
        calibrando = False
        visualizar_medicion()
    if selection.get() == 4: #CANNY CONTORNO
        rad1.configure(state='disabled')
        rad2.configure(state='disabled')
        rad3.configure(state='disabled')
        num_input = return_videoinput()
        cap = cv2.VideoCapture(num_input)
        slider_th1.set(30)
        slider_th2.set(80)
        slider_th1.grid(column=0,row=2)
        slider_th2.grid(column=0,row=3)
        btnLimpiar.grid(column=1,row=2)
        btnCapturar.grid(column=1,row=3)
        visualizar_canny()

def return_videoinput():
    return int(Combobox_Entrada.get())


#WIDGETS PARA LA INTERFAZ-------------------------------------------------------------------------------------------------------------------
root = Tk()#Ventana principal
root.title('TIMMYSOFT')
root.resizable(False, False)
#BOTONES RADIALES-----------------------------------------------------------------
selection = IntVar() #Variable de selección 1:Normal 2:Calibración 3:Medición
rad1 = Radiobutton(root,text='Procesamiento',width=13,value=1,variable=selection,command=que_se_selecciono)
rad2 = Radiobutton(root,text='Calibración',width=13,value=2,variable=selection,command=que_se_selecciono)
rad3 = Radiobutton(root,text='Medición',width=13,value=3,variable=selection,command=que_se_selecciono)
rad4 = Radiobutton(root,text='Canny',width=13,value=4,variable=selection,command=que_se_selecciono)
rad1.grid(column=0,row=0)
rad2.grid(column=1,row=0)
rad3.grid(column=2,row=0)
rad4.grid(column=3,row=0)
#LABEL VIDEO-----------------------------------------------------------------------
lblVideo = Label(root)
lblVideo.grid(column=0, row=1, columnspan=5)
lblVideo.bind('<Button-1>', pressed1)
lblVideo.bind('<ButtonRelease-1>', released1)
#SLIDERS---------------------------------------------------------------------------
slider_r = Scale(root,label='R', from_=0, to=255,orient='horizontal',width=10)
slider_g = Scale(root,label='G', from_=0, to=255,orient='horizontal',width=10)
slider_b = Scale(root,label='B', from_=0, to=255,orient='horizontal',width=10)
slider_contraste = Scale(root,label='Contraste', from_=1, to=5,orient='horizontal',resolution = 0.1,width=10)
slider_brillo = Scale(root,label='Brillo', from_=-150, to=100,orient='horizontal',width=10)
#CALIBRACIÓN----------------------------------------------------------------------
lblDistCalibrar = Label(root, text="Distancia para calibrar (mm):")
txtEntryDistCal = Entry(root, bd =5)
lblCteCal = Label(root,text="Constante de calibración (um/pixel):")
lblCteCal_val = Label(root,text="")
#MEDICIÓN---------------------------------------------------------------------------
lblCteCalMed = Label(root, text="Constante de calibración (um/pixel):")
lblCteCalMed_val = Label(root,text="")
#txtEntryCteCal= Entry(root, bd =5)
lblDistMed = Label(root,text="Distancia Medida (mm):")
lblDistMed_val = Label(root,text="")
lblScaleMax = Label(root,text="Escala máxima (mm):")
lblScaleMaxVal = Label(root,text="")
lblScale = Label(root,text="Escala deseada (mm):")
txtEntryScale = Entry(root, bd =5)
#LIMPIAR PANTALLA-------------------------------------------------------------------
btnLimpiar = Button(root,text='Limpiar pantalla',command=limpiar)
#FILTRO CANNY-----------------------------------------------------------------------
slider_th1 = Scale(root,label='Threshold 1', from_=0, to=255,orient='horizontal',width=10)
slider_th2 = Scale(root,label='Threshold 2', from_=0, to=255,orient='horizontal',width=10)
#CAPTURAR IMÁGENES------------------------------------------------------------------
btnCapturar = Button(root,text='Cápturar img',command=capturar)
#Entrada
Combobox_Entrada = ttk.Combobox(state="readonly",values=["0","1","2","3"])
Combobox_Entrada.set("0")
Combobox_Entrada.grid(column=4,row=0)
#Mainloop Ventana principal
root.mainloop()

#todo: si no se tiene algún valor en los txtentry (distancia conocida y cte de calibración) debe saltar un msg 

#todo: Histograma

