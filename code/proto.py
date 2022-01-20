import sys
import os
import cv2
import numpy as np
import time
from analyseContour import *
from filtrage import *

#Checking that this script is running on python2.7
print("Using python"+str(sys.version_info.major)+"."+str(sys.version_info.minor)) 

assert sys.version_info.major == 2 and sys.version_info.minor == 7
assert cv2.__version__=="4.2.0"
assert np.__version__=="1.13.3"


#in :  image_raw = image prise par le robot [ici RGB mais surement GRAY]
#in :  image_filtered = image filtree [NOIR et BLANC]
def func_preprocess(image_raw):
    return filtrage.preprocess(image_raw)


#int : image_edges               = image du coutour du trou [NOIR et BLANC]
#      expected_hole_radius    = rayon suppose du trou [FLOAT] (data optenue par autre pole que nous)
#out : is_defective              = indique si le trou est bon ou pas [BOOL] 
#      defect_type               = precise si possible de type de defaut [STR] 
def func_edge_analysis(image_edges,expected_hole_radius):
    return analyseContour.caracterization(cv2.cvtColor(image_edges,cv2.COLOR_GRAY2RGB),expected_hole_radius)

if __name__ == "__main__":
    curent_dir = os.getcwd()
    image_dir = curent_dir+"/images"
    print(image_dir)
    image_list = []
    for file in os.listdir(image_dir):
        if file.endswith(".jpg"):
            image_list.append(os.path.join(image_dir, file))

    rayons = [53,53,65,54,37,180,21,8,35,53,21]
    index = 0
    #for all the images we have
    for image_path in image_list:
        
        #0 LOADING OPENCV IMAGE

        image_raw = cv2.imread(image_path)
        cv2.imshow('image_raw',image_raw)
        start_time = time.time()
        
        #1 PREPROCESSING
        image_filtered=func_preprocess(image_raw)
        cv2.imshow('image_filtered',image_filtered)

        #2 CHECK
        is_defective,hole_type  = func_edge_analysis(image_filtered,rayons[index])
        print("is_defective : {}".format(is_defective))
        print("hole_type : {}".format(hole_type))

        #display infos
        contours, hierarchy = cv2.findContours(image_filtered, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if(is_defective):
            cv2.drawContours(image_raw, contours, -1, (0,0,255), 3)
        else:
            cv2.drawContours(image_raw, contours, -1, (0,255,0), 3)

        cv2.imshow('RESULT IHM',image_raw)

        print("--- TIME : %s seconds ---" % (time.time() - start_time))
        index+=1
        print("(press a key to process next image)")
        cv2.waitKey(0)