import pandas as pd
from glob import glob
import sys
import os
import shutil
import cv2
import argparse
parser = argparse.ArgumentParser(description="path files input and out file and csv file add resesize value and size "
                                             "or it will take default values")
parser.add_argument("--input",metavar="in",type=str,help=" input file path")
parser.add_argument("--output",metavar="out",type=str,help=" out file path")
parser.add_argument("--csv",metavar="csv",type=str,help=" csv file path")
parser.add_argument("--resize",metavar="r",type=int,help=" input file path")
parser.add_argument("--size",metavar="s",type=int,help=" input file path")
args = parser.parse_args()
print(args)
data = pd.read_csv(args.csv)
data.index = data["Img"]
data = data.drop(columns=["Img"],axis = 1)
folder_name = args.input
out_path = args.output
resize_size = args.resize
crop_size = args.size
images_offsets = []
folder_name = os.path.join(folder_name,"*")
#%%
try:
    shutil.rmtree(out_path)
    print("Removing and creating new file")
    os.mkdir(out_path)
except:
    print("No file found.It's okay Creating folder")
    os.mkdir(out_path)
for folder in glob(folder_name):
    files_name = os.path.join(folder, "*")
    crop_name = folder.split("/")[-1]
    print(crop_name)
    out_path = os.path.join(out_path, crop_name)
    os.mkdir(out_path)
    print(out_path)
    for img_path in glob(files_name):
        img_name = img_path.split("/")[-1]

        x_tar, y_tar = data.loc[img_name, "target_x"], data.loc[img_name, "target_y"]
        print(x_tar, y_tar)
        if abs(x_tar) <= 150 and abs(y_tar) <= 150:
            img = cv2.imread(img_path, cv2.IMREAD_COLOR);

            yb, xb, bb = img.shape
            img = cv2.resize(img, (resize_size, resize_size))
            h_crop = crop_size
            w_crop = crop_size
            y, x, b = img.shape

            if abs(x_tar) == 0 and abs(y_tar) == 0:
                stratx = ((x // 2) - (h_crop // 2))
                straty = ((y // 2) - (w_crop // 2))
                img = img[straty:straty + h_crop, stratx:stratx + w_crop]
                s = os.path.join(out_path, img_name)
                raw_s = r'{}'.format(s)
                print(os.path.join(out_path, img_name))

                writeStatus = cv2.imwrite(s, img)
                if writeStatus is True:
                    print("image written")
                else:
                    print("problem")

            else:
                stratx = ((x // 2) - (h_crop // 2)) + ((int(xb // resize_size)) + (y_tar))
                straty = ((y // 2) - (w_crop // 2)) + ((int(yb // resize_size)) + (x_tar))
                img = img[straty:straty + h_crop, stratx:stratx + w_crop]
                s = os.path.join(out_path, img_name)
                raw_s = r'{}'.format(s)
                print(os.path.join(out_path, img_name))
                writeStatus = cv2.imwrite(s, img)
                if writeStatus is True:
                    print("image written")
                else:
                    print("problem")

        else:
            offs = y_tar
            images_offsets.append(offs)

