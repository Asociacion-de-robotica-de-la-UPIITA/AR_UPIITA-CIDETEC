import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
#from __future__ import print_function
#from imutils.object_detection import non_max_suppression
#from imutils import paths
import numpy as np
#import argparse
#import imutils
import cv2, cv_bridge
from std_msgs.msg import Int32
from geometry_msgs.msg import Pose
#----------------------------------------------------------------------------------------------
import torch
x = torch.rand(5, 3)
print(x)



def callback(msg):
	pose_ventana = Pose()
	bridge = cv_bridge.CvBridge()
	imagen = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
	
	hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
	 
	#Rango de colores detectados:
	#Rojos:
	#rojo_bajos1 = np.array([160,70,70], dtype=np.uint8)
	#rojo_altos1 = np.array([180, 255, 255], dtype=np.uint8)
	#___________________________VENTANA_______________________________________--
	anaranjados1 = np.array([5,210,150], dtype=np.uint8)  
	#anaranjados1 = np.array([5,199,121], dtype=np.uint8)  		
	anaranjados2 = np.array([15,219,201], dtype=np.uint8)  
	#___________________________PARED_______________________________________--	
	pared1 = np.array([9,2,130], dtype=np.uint8)  
	#anaranjados1 = np.array([5,199,121], dtype=np.uint8)  		
	pared2 = np.array([29,22,210], dtype=np.uint8) 
	

        #Crear las mascaras
	#mascara_rojo1 = cv2.inRange(hsv, rojo_bajos1, rojo_altos1)
        mascara_naranja1 = cv2.inRange(hsv, anaranjados1, anaranjados2)
	mascara_pared = cv2.inRange(hsv, pared1, pared2)
	#ventana = cv2.bitwise_and(imagen,imagen, mask= mascara_rojo1) 
	ventana = cv2.bitwise_and(imagen,imagen, mask= mascara_naranja1)
	#ventana = cv2.bitwise_and(imagen,imagen, mask= mascara_pared)
	
	#rellena los huecos desde 11 x 11
	kernel=np.ones((27,27),np.uint8)
	dilation = cv2.dilate(ventana,kernel,iterations = 1)
	#cv2.imwrite("dil.jpg", dilation)
	#elimina los puntos
	kernel1=np.ones((27,27),np.uint8)
	opening = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel1)
	#convertimos a escala de grises
	gris = cv2.cvtColor(opening, cv2.COLOR_BGR2GRAY)
	gris = gris.astype('uint8')
	#plt.imshow(gris)
	#cv2.imwrite("gris.jpg", gris)
	#print(gris.shape)
	x,y,w,h=cv2.boundingRect(gris)
	rectangulo = cv2.rectangle(gris,(x,y),(x+w,y+h),(255,255,255),3)
	#plt.imshow(rectangulo)
	#cv2.imwrite("rect.jpg", rectangulo)

	##c1=int(x+w/2)
	##c2=int(y+h/2)
	##circulo = cv2.circle(gris,(int(x+w/2),int(y+h/2)),5,(255,255.255),-1)
	#plt.imshow(circulo)
	#cv2.imwrite("circ.jpg", circulo)
	##print('Las coordenadas del centro son:')
	##print(c1,c2)
	##pose_ventana.position.x = c1
	##pose_ventana.position.y = c2
	##pub.publish(pose_ventana)

	cv2.imshow('window', imagen)
        ##cv2.imshow('window2', imagen)
        cv2.imshow('window2', opening)
	cv2.imshow('window3', rectangulo)
        cv2.waitKey(1)

def detect_window():
	msg = rospy.Subscriber('bebop/image_raw', Image, callback, queue_size = 10)



if __name__ == '__main__':
	detect_window()
	rospy.init_node('ventana_node', anonymous = False)
	pub = rospy.Publisher('publish_ventana', Pose, queue_size=10)
	rate = rospy.Rate(10);
	rospy.spin()
