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

    show_steps = False

    curent_dir = os.getcwd()
    image_dir = curent_dir+"/images_robot"
    print(image_dir)
    image_list = []
    for file in os.listdir(image_dir):
        if file.endswith(".bmp"):
            image_list.append(os.path.join(image_dir, file))

    rayons = [246,242,580,415,392,415,417,596,145,150]
    index = 0
    #for all the images we have
    for image_path in image_list:
        
        #0 LOADING OPENCV IMAGE

        image_raw = cv2.imread(image_path)
        #image_raw_resized = cv2.resize(image_raw,(520,388))
        if(show_steps):
            cv2.imshow('image_raw',image_raw)
        start_time = time.time()
        
        load_time = (time.time() - start_time)
        print("--- LOADING TIME : %s seconds ---" % (time.time() - start_time))


        #1 PREPROCESSING
        image_filtered=func_preprocess(image_raw)
        if(show_steps):
            cv2.imshow('image_filtered',image_filtered)

        preprocess_time = (time.time() - start_time) - load_time
        print("--- PREPROCESS TIME : %s seconds ---" % preprocess_time)

        #2 CHECK
        is_defective,hole_type,contours  = func_edge_analysis(image_filtered,rayons[index])
        print("is_defective : {}".format(is_defective))
        print("hole_type : {}".format(hole_type))

        an_time = (time.time() - start_time) - preprocess_time
        print("--- ANALYSE TIME : %s seconds ---" % an_time)

        cv2.putText(image_raw, hole_type, (50,130), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 255), 5, cv2.LINE_AA)
        #display infos
        if(is_defective):
            cv2.drawContours(image_raw, contours, -1, (0,0,255), 15)
        else:
            cv2.drawContours(image_raw, contours, -1, (0,255,0), 15)

    
        cv2.imshow('RESULT IHM',cv2.resize(image_raw,(520,388)))

        print("--- FINISH TIME : %s seconds ---" % (time.time() - start_time))
        index+=1
        print("(press a key to process next image)")
        cv2.waitKey(0)
