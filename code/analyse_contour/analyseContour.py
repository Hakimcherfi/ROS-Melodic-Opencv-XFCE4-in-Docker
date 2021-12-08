#!/usr/bin/python
import numpy as np
import cv2
assert cv2.__version__=="4.2.0"

def contour(image):
    grey = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) #conversion greyscale
    ret,im_thresh = cv2.threshold(grey,127,255,cv2.THRESH_BINARY)
    contours,hierarchy = cv2.findContours(im_thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    assert (len(contours)==1),"plusieurs contours detectes"
    contours = contours[0]
    moments = cv2.moments(contours)
    x = moments['m10']/moments['m00']
    y = moments['m01']/moments['m00']
    aire = moments['m00']
    x,y,aire = np.round(x).astype("int"),np.round(y).astype("int"),np.round(aire).astype("int")
    return contours,x,y,aire

def cercle(image):
    grey = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) #conversion greyscale
    method = cv2.HOUGH_GRADIENT
    dp = 1 #0.5 : step 2 fois plus grand que resolution image. 2 : step 2 fois plus petit que resolution image
    minDist = 100000 #distance minimale entre cercles detectes (detecter cercle unique si assez grand, voir aucun si trop grand) mais le premier est conserve...
    param1 = 1#	seuil superieur donne a canny (seuil inf= moitie seuil sup)
    param2 = 1# seuil inferieur utilise pour mecanisme de vote (si bas, des faux cercles sont detectes)
    minRadius = 0#seuil inf des cercles recherches
    maxRadius = 0#seuil sup des cercles recherches (si <=0 utilise +gde dimension de l'image, si <0, retourne centres sans donner de rayons)
    circles = cv2.HoughCircles(grey,method,dp,minDist,param2 = param2) #liste de tuples contenant coordonnees cercles et votes
    return circles[:1,:1,:].reshape(1,3)

def caracterization(image,rayon,affichage=False):
    """
    fonction caracterization
    in :
    -image (numpy array) binaire du contour unique et ferme du trou (contour a 255, fond a 0)
    -rayon suppose du trou dans image
    -affichage : booleen pour creer fenetre affichage des differentes etapes
    out :
    - isdefective : booleen
    - defect : string contenant une forme/defaut reconnue
    """
    isdefective = False
    defect = ""
    circle = cercle(image)
    if circle is None:
        print("no circle found.")
        return True,"no circle found."
    contours,xbar,ybar,aire = contour(image)
    if contours is None:
        print("issue with contours detection.")
        return True,"issue with contours detection."
    #caracterisation :

    #entre hough et les contours (la forme est-elle un cercle ?)
    if (np.pi*(circle[:,2:])**2)*0.9<=aire<=np.pi*((circle[:,2:])**2)*1.1:
        pass
    else:
        isdefective=True
        defect = "area mismatch cercle/contours ({}/{})\n".format(float(np.pi*((circle[:,2:])**2)),aire)
    
    if (circle[:,2:]*0.9<=rayon<=circle[:,2:]*1.1):
        pass
    else:
        isdefective=True
        defect += "radius mismatch function parameter/cercle ({}/{})\n".format(rayon,float(circle[:,2:]))
    
    if affichage:
        cv2.imshow('original image',image)
        cv2.waitKey(0)
        output = image.copy()
        circle = np.round(circle[:, :]).astype("int") #pixels : valeurs entieres
        cv2.circle(output,(circle[:,:1],circle[:,1:2]),circle[:,2:],(0,0,255),1) #dessine cercle
        cv2.imshow('transfo hough',output)
        cv2.waitKey(0)
        output = np.zeros(image.shape)
        output = cv2.drawContours(image=output,contours=contours,contourIdx=-1,color=(0,0,255))
        cv2.imshow('contours',output)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return isdefective, defect

if __name__ == "__main__":
    image = cv2.imread('ovale.jpg')
    defect,resultat = caracterization(image,100,True)
    print(defect)
    print(resultat)