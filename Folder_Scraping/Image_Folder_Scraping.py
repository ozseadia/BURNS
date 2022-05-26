# -*- coding: utf-8 -*-
"""
Created on Mon May 23 09:27:58 2022

@author: OzSea
"""
import string
import os
from PIL import Image
import io
import hashlib
import random
#import path
import sys
Path=os.path.join((os.path.split(os.path.dirname(os.path.abspath(__file__))))[0],'Avoid_duplicates')
print(Path)
print (type(Path))
sys.path.append(Path)
#sys.path.append(r"G:\Oz\fiveer\Dani_Velinchick\Burns\Avoid_duplicates")
import Avoid_duplicates as AD
import MetaData as MD
from openpyxl.workbook import Workbook
import shutil
import glob


    
def main(folder_path,Images_Dir,Label):
    ad=AD.FeatureExtractor()
    md=MD.MetaData((os.path.split(Images_Dir))[0])
    path=folder_path
    image_files = glob.glob("%s/*.*" % path)
    for file in image_files:
        Flag=1
        try:
            image = Image.open(file).convert('RGB')
        except:
            Flag=0
        if Flag:    
            FlagSave=ad.main(image)
            if FlagSave:
                S=15 # file name length
                image_file_name=os.path.join(Images_Dir,''.join(random.choices(string.ascii_letters + string.digits, k = S)))
                split_tup = os.path.splitext(file)
                extension=split_tup[1]
                shutil.copy(file,image_file_name + extension)
                Info=[(os.path.split(image_file_name+ extension))[1],
                      str((image.size)),
                      "",
                      os.path.basename(Images_Dir),
                      "",
                      "",
                      "",
                      "",#PDFinfo.title,
                      "",#PDFinfo.author
                      "",#is Human
                      "",#is child
                      "",#Burn
                      Label]#Abuse Burn
                md.MetaDataAppend(Info)
        
        
            pass