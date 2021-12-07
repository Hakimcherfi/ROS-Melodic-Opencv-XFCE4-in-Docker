import numpy as np
import cv2
assert cv2.__version__ == "4.2.0"

im = cv2.imread('closed_form.jpg',1)
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret,im_thresh = cv2.threshold(imgray,127,255,cv2.THRESH_BINARY)
cv2.imshow('in',im)
cv2.waitKey(0)

cv2.imshow('seuil',im_thresh)
cv2.waitKey(0)

contours,hierarchy = cv2.findContours(im_thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
im_contours = np.zeros(im.shape)
im_contours = cv2.drawContours(image=im_contours,contours=contours,contourIdx=-1,color=(0,0,255))
assert contours is not None
for contour in contours:
    print(contour.shape)
    moments = cv2.moments(contour)
    x,y = np.round(moments['m10']/moments['m00']).astype("int"),np.round(moments['m01']/moments['m00']).astype("int")
    im_contours = cv2.circle(im_contours,(x,y),radius=1,color=(0,0,255))
    print(moments)

#normalization manuelle
i_min = np.amin(im_contours)
i_max = np.amax(im_contours)
#im_contours = (im_contours-i_min)/(i_max-i_min)*255
#im_contours = cv2.normalize(im_contours,im_contours,0,255,cv2.NORM_MINMAX)

cv2.imshow('contours',im_contours)
cv2.waitKey(0)