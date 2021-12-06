import sys
import os
import cv2
import numpy as np
import time

#Checking that this script is running on python2.7
print("Using python"+str(sys.version_info.major)+"."+str(sys.version_info.minor)) 
assert sys.version_info.major == 2 and sys.version_info.minor == 7


#in :  image_raw = image prise par le robot [ici RGB mais surement GRAY]
#in :  image_filtered = image filtree [NOIR et BLANC]
def func_preprocess(image_raw):
    image_filtered = cv2.cvtColor(image_raw, cv2.COLOR_BGR2GRAY)
    image_filtered = cv2.equalizeHist(image_filtered)
    image_filtered = cv2.medianBlur(image_filtered, 25)
    kernel0 = np.ones((5, 5), np.uint8)
    image_filtered = cv2.dilate(image_filtered, kernel0)
    image_filtered = cv2.erode(image_filtered, kernel0)
    return image_filtered

#in :  image_filtered = image filtree [NOIR et BLANC]
#out : image_edges    = image du coutour du trou [NOIR et BLANC]
def func_edge_detection(image_filtered):
    image_edges = None
    return image_edges

#int : image_edges               = image du coutour du trou [NOIR et BLANC]
#      expected_hole_diameter    = diametre suppose du trou [FLOAT] (data optenue par autre pole que nous)
#out : is_defective              = indique si le trou est bon ou pas [BOOL] 
#      defect_type               = precise si possible de type de defaut [STR] 
def func_edge_analysis(image_edges,expected_hole_diameter):
    defect_type = "square"
    is_defective = True
    return is_defective,defect_type



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
        cv2.imshow('image_raw',image_raw)
        start_time = time.time()
        #1 PREPROCESSING
        image_filtered=func_preprocess(image_raw)
        cv2.imshow('image_filtered',image_filtered)

        #2 EDGE FILTERING 
        #   Je vais rapidement fournir une V0 de la fonction de filtrage 
        #   en attendant tu peux essayer sur des images non filtrees  
        image_edges=func_edge_detection(image_filtered)


        #3 EDGE ANALYSIS 
        #   En attendant que guilhem vous sorte une image des contours
        #   vous devrez bosser sur une image paint  
        is_defective,hole_type  = func_edge_analysis(image_edges,8)
        print("--- TIME : %s seconds ---" % (time.time() - start_time))

        print("(press a key to process next image)")
        cv2.waitKey(0)



