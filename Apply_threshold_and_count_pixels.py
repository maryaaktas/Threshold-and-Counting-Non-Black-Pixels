# Marya Aktaş 200444001 - Term Project

import cv2
import numpy as np
from tkinter import *
from PIL import Image,ImageTk
from abc import ABC, abstractmethod

cap = cv2.VideoCapture(0)

win = Tk()
win.title('Term Project')

frame1 = LabelFrame(win)
frame1.grid(column=0, row=0)

PicLabel = Label(frame1)
PicLabel.grid(column=0, row=0)

frame2 = Frame(win)
frame2.grid(column=0, row=1)

frame3 = Frame(win)
frame3.grid(column=1, row=0)

frame4 = Frame(win)
frame4.grid(column=0, row=2)

LH = Scale(frame2, from_=0, to=255, orient=HORIZONTAL, length=450, sliderlength=10)
UH = Scale(frame2, from_=0, to=255, orient=HORIZONTAL, length=450, sliderlength=10)
UH.set(255)
LS = Scale(frame2, from_=0, to=255, orient=HORIZONTAL, length=450, sliderlength=10)
US = Scale(frame2, from_=0, to=255, orient=HORIZONTAL, length=450, sliderlength=10)
US.set(255)
LV = Scale(frame2, from_=0, to=255, orient=HORIZONTAL, length=450, sliderlength=10)
UV = Scale(frame2, from_=0, to=255, orient=HORIZONTAL, length=450, sliderlength=10)
UV.set(255)
Thresh = Scale(frame2, from_=0, to=255, orient=HORIZONTAL, length=450, sliderlength=10)
Thresh.set(255)

scale_list = [LH, UH, LS, US, LV, UV, Thresh]
label_list = ['LH: ', 'UH: ', 'LS: ', 'US: ', 'LV: ', 'UV: ', 'Threshold: ']
for i in range(7):
    Label(frame2, text=label_list[i]).grid(column=0,row=i)
    scale_list[i].grid(column=1, row=i)

b1 = Button(frame3, text='Apply\nThreshold', bg='#F60A0A', fg='black')
b2 = Button(frame3, text='Calculate For\nRegion 1', bg='#89AFD5', fg='black')
b3 = Button(frame3, text='Calculate For\nRegion 2', bg='#89AFD5', fg='black')
b4 = Button(frame3, text='Calculate For\nRegion 3', bg='#89AFD5', fg='black')

button_list = [b1, b2, b3, b4]
for i in range(4):
    button_list[i].grid(column=0,row=i, sticky=W + E + N + S, ipadx=5)

message = StringVar()
message.set('Press Any Button')
calculate = Label(frame4, textvariable=message, relief=FLAT, bg='pale violet red', fg='black')
calculate.pack(expand=YES, fill=BOTH, ipady=10, ipadx=10)

class Frame_Grab(ABC):
    def __init__(self):
        self.frame = cap.read()[1]
        self.hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)

class Sliders_Data(ABC):
    def Set_Slider_Data(self):
        self.__l_b = np.array([LH.get(), LS.get(), LV.get()])
        self.__u_b = np.array([UH.get(), US.get(), UV.get()])

    def Get_Slider_Data(self):
        return self.__l_b, self.__u_b

class Region1(Frame_Grab, Sliders_Data):
    def __init__(self,res_HSV):
        self.res_HSV = res_HSV

    def Pixel_Calculation(self):
        a = self.res_HSV.shape[0]  #y
        b = self.res_HSV.shape[1]  #x
        c = self.res_HSV.shape[2]  #channel
        self.PixelNO = 0

        for y in range(a):
            for x in range(b//3):
                for z in range(c):
                    if self.res_HSV[y, x, z] != 0:
                        self.PixelNO = self.PixelNO + 1
        message.set('The pixel number of Region 1 is: {}'.format(self.PixelNO))

class Region2(Frame_Grab,Sliders_Data):
    def __init__(self, res_HSV):
        self.res_HSV = res_HSV

    def Pixel_Calculation(self):
        a = self.res_HSV.shape[0]
        b = self.res_HSV.shape[1]
        c = self.res_HSV.shape[2]
        self.PixelNO=0

        for y in range(a):
            for x in range(int(b / 3), int(2 * (b / 3))):
                for z in range(c):
                    if self.res_HSV[y, x, z] != 0:
                        self.PixelNO = self.PixelNO + 1
        message.set('The pixel number of Region 2 is: {}'.format(self.PixelNO))

class Region3(Frame_Grab, Sliders_Data):
    def __init__(self, res_HSV):
        self.res_HSV=res_HSV

    def Pixel_Calculation(self):
        a = self.res_HSV.shape[0]
        b = self.res_HSV.shape[1]
        c = self.res_HSV.shape[2]
        self.PixelNO = 0

        for y in range(a):
            for x in range(int(2 * (b / 3)), b):
                for z in range(c):
                    if self.res_HSV[y, x, z] != 0:
                        self.PixelNO = self.PixelNO + 1
        message.set('The pixel number of Region 3 is: {}'.format(self.PixelNO))

class Filter(Frame_Grab,Sliders_Data):
    def Filter_Implement(self):
        while True:
            self.frame1 = cap.read()[1]
            self.frame1_gray = cv2.cvtColor(self.frame1, cv2.COLOR_BGR2GRAY)
            th_val = Thresh.get()
            _, thresh_trunc = cv2.threshold(self.frame1_gray, th_val, 255, cv2.THRESH_TRUNC)
            cv2.putText(thresh_trunc, 'Press ESC for going to the other window', (int(x // 4), 20), font, 0.5, (147, 112, 219), 2)
            cv2.imshow('Thresholded Camera', thresh_trunc)
            if cv2.waitKey(1) & 0xFF == 27:
                break
        cv2.destroyAllWindows()

Slider = Sliders_Data()
filter = Filter()

while True:
    Frame_obj = Frame_Grab()
    frame = Frame_obj.frame
    hsv = Frame_obj.hsv

    Slider.Set_Slider_Data()

    l_b = Slider.Get_Slider_Data()[0]
    u_b = Slider.Get_Slider_Data()[1]

    mask1 = cv2.inRange(hsv, l_b, u_b)
    res = cv2.bitwise_and(frame, frame, mask=mask1)

    res_HSV = cv2.cvtColor(res, cv2.COLOR_BGR2HSV)

    region1 = Region1(res_HSV)
    region2 = Region2(res_HSV)
    region3 = Region3(res_HSV)

    b1.configure(command=filter.Filter_Implement)
    b2.configure(command=region1.Pixel_Calculation)
    b3.configure(command=region2.Pixel_Calculation)
    b4.configure(command=region3.Pixel_Calculation)

    frameRGB = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)

    x = frameRGB.shape[1]
    y = frameRGB.shape[0]

    cv2.line(img=frameRGB, pt1=(x // 3, 0), pt2=(x//3, y), color=(255 , 0, 0), thickness=3, lineType=8, shift=0)
    cv2.line(img=frameRGB, pt1=(2*(x // 3), 0), pt2=(2*(x // 3), y), color=(255, 0, 0), thickness=3, lineType=8, shift=0)

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frameRGB, 'Region 1', (int(x // 8), 20), font, 0.5, (219, 112, 147), 2)
    cv2.putText(frameRGB, 'Region 2', (int(3.5*(x // 8)), 20), font, 0.5, (219, 112, 147), 2)
    cv2.putText(frameRGB, 'Region 3', (int(6.3*(x // 8)), 20), font, 0.5,  (219, 112, 147), 2)

    img = ImageTk.PhotoImage(Image.fromarray(frameRGB))
    PicLabel['image'] = img

    win.update()

cap.release()
