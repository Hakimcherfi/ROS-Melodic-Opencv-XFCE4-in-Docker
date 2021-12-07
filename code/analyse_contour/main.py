#!/usr/bin/python
import numpy as np
import cv2
assert cv2.__version__=="4.2.0"

def fonction(image):
	output = image.copy() #pour affichage
	grey = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) #conversion greyscale
	assert np.amax(grey) == 255
	#ret,threshold = cv2.threshold(grey,127,255,0)
	mode = 1
	method = 2
	contours,hierarchy = cv2.findContours(grey,mode,method)
	#cv2.imshow('figure',cv2.Canny(grey,10,100))
	#cv2.waitKey(0)
	
	#parametres houghcircle :
	method = cv2.HOUGH_GRADIENT
	dp = 1 #0.5 : step 2 fois plus grand que resolution image. 2 : step 2 fois plus petit que resolution image
	minDist = 100000 #distance minimale entre cercles detectes (detecter cercle unique si assez grand, voir aucun si trop grand)
	param1 = 1#	seuil superieur donne a canny (seuil inf= moitie seuil sup)
	param2 = 1# seuil inferieur utilise pour mecanisme de vote (si bas, des faux cercles sont detectes)
	minRadius = 0#seuil inf des cercles recherches
	maxRadius = 0#seuil sup des cercles recherches (si <=0 utilise +gde dimension de l'image, si <0, retourne centres sans donner de rayons)
	circles = cv2.HoughCircles(grey,method,dp,minDist,param2 = param2) #liste de tuples contenant coordonnees cercles et votes
	
	if circles is not None:
		circles = np.round(circles[0, :]).astype("int") #conversion en entiers
		#boucle sur cercle trouves
		for (x, y, r) in circles:
			cv2.circle(output,(x,y),r,(0,0,255),1) #dessine cercle
		cv2.imshow('out',output)
		cv2.waitKey(0)
	else:
		print("no circle found.")
	
	

image = cv2.imread('closed_form.jpg')
cv2.imshow('original',image)
cv2.waitKey(0)
cercles = fonction(image)
cv2.destroyAllWindows()