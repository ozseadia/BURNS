# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 16:16:03 2022

@author: OzSea
"""

#Avoid_duplicates
# Import the libraries
#import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
#from pathlib import Path
from PIL import Image
import os

class FeatureExtractor:
    def __init__(self):
        # Use VGG-16 as the architecture and ImageNet for the weight
        base_model = VGG16(weights='imagenet')
        # Customize the model to return features from fully-connected layer
        self.model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)
        self.FDB=os.path.join(os.path.dirname(__file__),'DataBase_features.npy') # Features database file path
    def extract(self, img):
        # Resize the image
        img = img.resize((224, 224))
        # Convert the image color space
        img = img.convert('RGB')
        # Reformat the image
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        # Extract Features
        feature = self.model.predict(x)[0]
        return feature / np.linalg.norm(feature)
    def features_DataBase(self,Input_path,Output_path):
    # Iterate through images (Change the path based on your image location)
        #features=np.empty((0,4096)) 
        FlagC=0
        for img_path in sorted(os.listdir(Input_path)):
                print(img_path)
                # Extract Features
                temp=FeatureExtractor.extract(self,img=Image.open(os.path.join(Input_path,img_path)))
                if  FlagC==0: 
                    features=(np.reshape(temp,[1,len(temp)]))
                    #features=temp
                    
                else:
                    #features=np.append(features,temp,axis=0)
                    features =np.append(features,np.reshape(temp,[1,len(temp)]),axis=0)
                FlagC=1                      
                # Save the Numpy array (.npy) on designated path
                #feature_path = "<IMAGE FEATURE PATH HERE>.npy"
        feature_path = os.path.join(Output_path ,'DataBase_features.npy')
        np.save(feature_path, features)
        return features
     
    def Add_to_features_DataBase(self,Fvect):
        features=np.load(self.FDB)
        features =np.append(features,np.reshape(Fvect,[1,len(Fvect)]),axis=0)
        np.save(self.FDB, features)
        return
        
    
    def main(self,imag):
        FlagSave=0
        features=np.load(self.FDB)
        Fvect=FeatureExtractor.extract(self, imag)
        dists = np.linalg.norm(features - Fvect, axis=1)
        if not any(dists<0.5):
            FeatureExtractor.Add_to_features_DataBase(self,Fvect)
            FlagSave=1
        return FlagSave    
        
        
'''        
Input_path=r'G:\Oz\fiveer\Dani Velinchick\Burns\Scraping-Google-Images-using-Python-master\dataset\Child Burn'
Output_path=r'G:\Oz\fiveer\Dani Velinchick\Burns\Avoid_duplicates'
self=FeatureExtractor()
FeatureExtractor.features_DataBase(self,Input_path,Output_path)                
feature_path = os.path.join(Output_path ,'DataBase_features.npy')
features=np.load(feature_path)

# Insert the image query
img = Image.open(os.path.join(Input_path,'4daf787b1606c83.jpg'))
# Extract its features
query = FeatureExtractor.extract(self,img)
# Calculate the similarity (distance) between images
dists = np.linalg.norm(features - query, axis=1)
# Extract 30 images that have lowest distance
'''
'''
ids = np.argsort(dists)[:30]
scores = [(dists[id], img_paths[id]) for id in ids]
# Visualize the result
axes=[]
fig=plt.figure(figsize=(8,8))
for a in range(5*6):
    score = scores[a]
    axes.append(fig.add_subplot(5, 6, a+1))
    subplot_title=str(score[0])
    axes[-1].set_title(subplot_title)  
    plt.axis('off')
    plt.imshow(Image.open(score[1]))
fig.tight_layout()
plt.show()    
''' 
    