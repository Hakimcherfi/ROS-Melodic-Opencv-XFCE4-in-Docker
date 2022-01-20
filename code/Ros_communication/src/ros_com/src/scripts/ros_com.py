#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from std_msgs.msg import Float32
from analyseContour import analyseContour
import cv2
class RosCom:

    def __init__(self):
        #Subscriber pour recuperer l'image et la taille du trou
        self.trou_subscriber = rospy.Subscriber("/topic_trou",Float32,self.callbackTrou)
        self.image_subscriber = rospy.Subscriber("/topic_image",Image,self.callbackImage)
        
        #Publisher pour publier le rapport String formate JSON
        self.rapport_qualite_publisher = rospy.Publisher("topic_rapport_qualite",String,queue_size=1)
        
        self.rate = rospy.Rate(10) #10 Hz
        #Stocker la taille du trou
        self.tailles_trou = []
        
    def callbackImage(self,data): 
        image_trou = data
        taille_trou = self.tailles_trou[end]        
        #Apres traitement qualite on recupere un booleen pour la conformite et la raison si non conforme
        conforme,raison = analyseContour.caracterization(image_trou,taille_trou,False)
        
        rapport = "{conforme : " +str(conforme)+", raison : "+ raison +"}"
        self.rapport_qualite_publisher.publish(rapport)
        self.rate.sleep()
        
    def callbackTrou(self,data):
        taille_trou = data
        self.tailles_trou.append(taille_trou)
    
if __name__ == '__main__':    
    rospy.init_node('qualite_ros_com',anonymous=True)
    roscom = RosCom()    
    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
