##Load Library
import numpy as np, pandas as pd, gc
import cv2, matplotlib.pyplot as plt
import os
import glob

def image_preproc(input_train_path_csv, input_img_path, export_img_path, resize_size, crop_size):
    
    train_images = []
    train_labels = []
    images_offsets = []
    SIZE = resize_size
    
    train_csv = pd.read_csv(input_train_path_csv)
    img_path = train_csv['img_path']
    tar_x = train_csv['target_x']
    tar_y = train_csv['target_y']
    Label = train_csv['Labels']
    
    SampleNum = len(img_path)
    
    for i in range(SampleNum):
        impath = img_path[i]
        labeli = Label[i]
        x_tar = tar_x[i]
        y_tar = tar_y[i]
        
        
        if abs(x_tar) <= 150 and abs(y_tar) <= 150:
            img = cv2.imread(input_img_path.format(impath), cv2.IMREAD_COLOR)
            yb,xb,bb = img.shape
            img = cv2.resize(img, (SIZE, SIZE))
            h_crop = crop_size
            w_crop = crop_size
            y,x,b = img.shape
            
            if abs(x_tar) == 0 and abs(y_tar) == 0:
                stratx = ((x//2)-(h_crop//2))
                straty = ((y//2)-(w_crop//2))
                img = img[straty:straty+h_crop, stratx:stratx+w_crop]
                cv2.imwrite(export_img_path.format(impath), img)
                
            else:
                stratx = ((x//2)-(h_crop//2))+((int(xb//SIZE))+(y_tar))
                straty = ((y//2)-(w_crop//2))+((int(yb//SIZE))+(x_tar))
                img = img[straty:straty+h_crop, stratx:stratx+w_crop]
                cv2.imwrite(export_img_path.format(impath), img)
        
        else:
            offs = y_tar
            images_offsets.append(offs)
            
    return train_images, train_labels, images_offsets
    
