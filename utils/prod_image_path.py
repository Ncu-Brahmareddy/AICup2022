##Load Library
import numpy as np, pandas as pd
import cv2, matplotlib.pyplot as plt
import os
import glob

def prod_image_path(input_img_path,input_location_csv, export_csv_name):
    train_labels = []
    img_name_dic = []
    
    for directory_path in glob.glob(input_img_path):
        for img_pa in glob.glob(os.path.join(directory_path, "*.jpg")):
            img_dic = img_pa.split('\\')[-1]
            img_lbl = img_pa.split('\\')[1]
            img_name_dic.append(img_dic)
            train_labels.append(img_lbl)
    
    train_labels = np.array(train_labels)
    SampleNum = len(train_labels)
    sl = np.zeros(SampleNum).astype(str)
    sl[:] = '/'
    start_path = np.char.add(train_labels, sl)
    img_path = np.char.add(start_path, img_name_dic)
    train_labels = pd.DataFrame(train_labels, columns=['Labels'])
    img_path = pd.DataFrame(img_path, columns=['img_path'])
    img_name_dic = pd.DataFrame(img_name_dic, columns=['Img'])
    
    loc_data = pd.read_csv(input_location_csv)
    loc_data = loc_data.merge(img_name_dic, on=['Img'])
    loc_data = pd.concat([loc_data, img_path], axis=1, join='inner')
    loc_data = pd.concat([loc_data, train_labels], axis=1, join='inner')
    loc_data.to_csv(export_csv_name,index=False)
    
    return loc_data
