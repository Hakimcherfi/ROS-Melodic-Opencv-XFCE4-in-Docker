import sys
import os
import cv2
import numpy as np
import time
from analyseContour import *

#Checking that this script is running on python2.7
print("Using python"+str(sys.version_info.major)+"."+str(sys.version_info.minor)) 
assert sys.version_info.major == 2 and sys.version_info.minor == 7


#in :  image_raw = image prise par le robot [ici RGB mais surement GRAY]
#in :  image_filtered = image filtree [NOIR et BLANC]
def func_preprocess(image_raw):

    image_filtered = cv2.cvtColor(image_raw, cv2.COLOR_BGR2GRAY)
    image_filtered = cv2.medianBlur(image_filtered, 25)
    cv2.imshow('test',image_filtered)
    image_filtered = cv2.adaptiveThreshold(image_filtered,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,41,10)

    des = cv2.bitwise_not(image_filtered)
    contour,hier = cv2.findContours(des,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contour:
        cv2.drawContours(des,[cnt],0,255,-1)

    image_filtered = cv2.bitwise_not(des)
    return cv2.bitwise_not(image_filtered) 

#in :  image_filtered = image filtree [NOIR et BLANC]
#out : image_edges    = image du coutour du trou [NOIR et BLANC]
def func_edge_detection(image_filtered):

    # Sobel Edge Detection    
    # sobelxy = cv2.Sobel(src=image_filtered, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5) # Combined X and Y Sobel Edge Detection
    # # Display Sobel Edge Detection Images    
    # cv2.imshow('Sobel Edge Detection', sobelxy)
    # cv2.waitKey(0)

    # Canny Edge Detection
    edges = cv2.Canny(image_filtered,100,300,3) # Canny Edge Detection
    # Display Canny Edge Detection Image
    cv2.imshow('Canny Edge Detection', edges)

    #Laplacian Edge Detection
    # laplacian = cv2.Laplacian(image_filtered,cv2.CV_64F)
    # cv2.imshow('Laplacian Edge Detection',laplacian)
    #cv2.waitKey(0)

#int : image_edges               = image du coutour du trou [NOIR et BLANC]
#      expected_hole_diameter    = diametre suppose du trou [FLOAT] (data optenue par autre pole que nous)
#out : is_defective              = indique si le trou est bon ou pas [BOOL] 
#      defect_type               = precise si possible de type de defaut [STR] 
def func_edge_analysis(image_edges,expected_hole_diameter):
    return analyseContour.caracterization(cv2.cvtColor(image_edges,cv2.COLOR_GRAY2RGB),expected_hole_diameter)



if __name__ == "__main__":
    curent_dir = os.getcwd()
    image_dir = curent_dir+"/images"
    print(image_dir)
    image_list = []
    for file in os.listdir(image_dir):
        if file.endswith(".jpg"):
            image_list.append(os.path.join(image_dir, file))

    #for all the images we have
    for image_path in image_list:
        
        #0 LOADING OPENCV IMAGE

        image_raw = cv2.imread(image_path)
        print(image_raw.shape)
        cv2.imshow('image_raw',image_raw)
        start_time = time.time()
        
        #1 PREPROCESSING
        image_filtered=func_preprocess(image_raw)
        cv2.imshow('image_filtered',image_filtered)

        #2 EDGE FILTERING 
        #   Je vais rapidement fournir une V0 de la fonction de filtrage 
        #   en attendant tu peux essayer sur des images non filtrees  
        #image_edges=func_edge_detection(image_filtered)


        #3 EDGE ANALYSIS 
        #   En attendant que guilhem vous sorte une image des contours
        #   vous devrez bosser sur une image paint  
        is_defective,hole_type  = func_edge_analysis(image_filtered,8)
        print("is_defective : {}".format(is_defective))
        print("hole_type : {}".format(hole_type))
        print("--- TIME : %s seconds ---" % (time.time() - start_time))

        print("(press a key to process next image)")
        cv2.waitKey(0)



