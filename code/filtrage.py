import os
import cv2
import numpy as np

class filtrage:
    @staticmethod
    def preprocess(image_raw):


        image_filtered = cv2.cvtColor(image_raw, cv2.COLOR_BGR2GRAY)
        image_filtered = cv2.medianBlur(image_filtered, 25)
        image_filtered = cv2.bitwise_not(image_filtered)


        image_filtered = cv2.adaptiveThreshold(image_filtered,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,1501,10)

        #cv2.imshow('pp1',cv2.resize(image_filtered,(520,388)))

        des = cv2.bitwise_not(image_filtered)
        contour,hier = cv2.findContours(des,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contour:
            cv2.drawContours(des,[cnt],0,255,-1)

        #image_filtered = cv2.bitwise_not(des)
        return cv2.bitwise_not(image_filtered)

