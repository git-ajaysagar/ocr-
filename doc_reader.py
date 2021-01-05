#The following is an OCR program that reads out text from an image using pytesseract and opencv

# -*- coding: utf-8 -*-
'''By Ajay'''

#imporitng required libraries
import requests
import pytesseract 
import cv2 as cv
import numpy as np
from PIL import Image,ImageEnhance
from gtts import gTTS
from playsound import playsound
import os
    
#reading image and preprocessing it   
image= cv.imread('string containing path to image')
x,y,z=image.shape
i=image
i=cv.cvtColor(i,cv.COLOR_BGR2GRAY)
r,c=i.shape
ratio_r,ratio_c=round(r/5.4),round(c/4.8)
c1,c2=round(r/2),round(c/2)
img=i[c1-int(ratio_r/2):c1+int(ratio_r/2),c2-int(ratio_c/2):c2+int(ratio_c/2)]
img=img.reshape(-1)
img=np.sort(img,axis=0)[:50]
thr=img.mean()
thr=thr.item()
thr=thr+50

_,im=cv.threshold(i,thr,255,cv.THRESH_TOZERO)

boxes=pytesseract.image_to_data(im)
row_s=[]
col_s=[]
for m,b in enumerate(boxes.splitlines()):
    if m!=0:
       b=b.split()
       if len(b)==12:
           x,y,w,h=int(b[6]),int(b[7]),int(b[8]),int(b[9])
           if x<10 or y<10 or w>c-10 or h>x-10:
               pass
           else:
               row_s.append(y)
               col_s.append(x)
               cv.rectangle(im,(x-1,y-1),(x+w+20,y+h+2),(0,0,255),5)
min_r=min(row_s)
max_r=max(row_s)
min_c=min(col_s)
max_c=max(col_s)
cv.rectangle(i,(min_c-10,min_r-10),(max_c+35,max_r+30),(0,255,0),3)
i_cropped=i[min_r-10:max_r+30,min_c-10:max_c+35]
print(type(i_cropped))
pil_im=Image.fromarray(i_cropped)
enha=ImageEnhance.Contrast(pil_im)
factor=1.5
contrasted=enha.enhance(factor)
np_img=np.array(contrasted)

#extracring text from image using pytesseact
text=pytesseract.image_to_string(np_img)
print(text)

#converting text to speech
speak=gTTS(text,lang='en')
speak.save('doc_reading.mp3')

#playing the text audio
playsound('doc_reading.mp3')
os.remove('doc_reading.mp3')   #removing audio after playing. 

