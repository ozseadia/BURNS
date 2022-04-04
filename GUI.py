# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 19:04:35 2022

@author: OzSea
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import Scraping_Google_Images.google_image_scraping_script as GIS
import PDF_Scraping.PDF_Images_Scraping as PIS
import sys 
import tkinter as tk
from tkinter import filedialog
import glob
Path=os.path.dirname(__file__)
sys.path.append(Path)
CurrentPath=__file__
st.title('Images DataBase Collection tool')

# Some number in the range 0-23
Method = st.sidebar.selectbox('Select Scraping Method', ['','Google Image','Google Scholar'
                                                , 'List of PDFs'])
class Scarping :
    # init method or constructor
   def __init__(self,Method,CurrentPath): 
   #    self.Method=Method
       self.Method=Method
       self.MainPath=os.path.dirname(CurrentPath)
       self.Chrome_path=os.path.join(os.path.dirname(CurrentPath),'chromedriver.exe') 
   def Google_Image(self):
        if self.Method=='Google Image':
            st.title(self.Method)
            n=st.text_input('Maximum number of images')
            List_Search_Keys = st.file_uploader("Upload List", type=["csv","xlsx"])
            if  List_Search_Keys:
                df = pd.read_excel(List_Search_Keys)
                if not (df['Key Words']).empty:
                    st.write('Not Empt')
                    queries=df['Key Words'].values.tolist()
                    st.write(self.Chrome_path)
                    GIS.main(queries,int(n)+2,self.Chrome_path,self.MainPath)
                
            
   #@st.cache         
   def Google_Scholar(self):
        if self.Method =='Google Scholar':
            st.title(self.Method)
            
   def List_of_PDFs(self):
        if self.Method =='List of PDFs':
            st.title(self.Method) 
                # import libraries
            root = tk.Tk()
            root.withdraw()
            
            # Make folder picker dialog appear on top of other windows
            root.wm_attributes('-topmost', 1)
            
            # Folder picker button
            st.title('Folder Picker')
            st.write('Please select a folder:')
            clicked = st.button('Folder Picker')
            if clicked:
                dirname = st.text_input('Selected folder:', filedialog.askdirectory(master=root))
                pdf_files = glob.glob("%s/*.pdf" % dirname)
                for file in pdf_files:
                    images_path =os.path.join(self.MainPath,'dataset')
                    new_abs_path = os.path.join(images_path, 
                                                os.path.basename(file)[:-4])
                    if not os.path.exists(new_abs_path):
                        os.mkdir(new_abs_path)
                    PIS.PDFs_Images_Extraction(file,new_abs_path)
                    #do_your_stuff()
                    
                
            
            
A=Scarping(Method,CurrentPath)
A.Google_Image()
A.Google_Scholar()
A.List_of_PDFs()
st.stop()


