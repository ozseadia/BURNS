# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 23:19:17 2022

@author: OzSea
"""
import string    
import random # define the random module     

import sys
import PyPDF2
from PyPDF2 import PdfFileReader
import os



def PDFs_Images_Extraction(pdf_path,Images_Dir):

    path=pdf_path
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
        info = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()
    
    with open(path, "rb") as file:
        pdf = file.read()
    
    img_counter = 0
    pointer = 0
    while True:
        pointer = pdf.find(b"stream", pointer)
        if pointer < 0:
            break
    
        x = pdf.find(b"\xff\xd8", pointer)
        if x < 0:
            pointer = pointer + 1
            continue
        else:
            extension = "jpg"
    
        limit = pdf.find(b"endstream", pointer)
        if limit < 0:
            break
    
        y = pdf.find(b"\xff\xd9", pointer, limit) + 2
    
        pointer = limit + 9
        if y < 2:
            continue        
        
        img = pdf[x:y]
    
        img_counter = img_counter + 1
        S=10 # file name length
        image_file_name=os.path.join(Images_Dir,''.join(random.choices(string.ascii_letters + string.digits, k = S))) 
        with open(image_file_name + "." + extension, "wb") as jpgfile:
            jpgfile.write(img)
            
pdf_path=r'G:\Oz\fiveer\Dani Velinchick\Burns\1302full.pdf'

script_path = os.path.dirname(__file__)
#basename = os.path.basename(pdf_path)[:,-4]

new_abs_path = os.path.join(script_path, os.path.basename(pdf_path)[:-4])
os.mkdir(new_abs_path)
PDFs_Images_Extraction(pdf_path,new_abs_path)