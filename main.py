import particle as pp
import cv2
import numpy as np
import matplotlib.pyplot as plt
######################################################################

def draw_rectangle(event, x, y, flags, params):
    global x_init, y_init, drawing, EtalonHist
    if event == cv2.EVENT_LBUTTONDOWN:
       drawing = False
       x_init, y_init = x, y
       EtalonHist = pp.CalculateHist(img,y_init,x_init)
       


##############################################################################
#img = cv2.imread('table.jpg',1)

		
cap = cv2.VideoCapture('table.mp4')



x_init, y_init = 1,1
drawing = True

cv2.namedWindow('frame')
cv2.setMouseCallback('frame', draw_rectangle)



count = 0
while(cap.isOpened()):
       ret, img = cap.read()
       if  drawing == False:
           count +=  1
           if  count == 1: 
               Cloud = pp.CreateParticles(x_init,y_init)
               Cloud.normalise(oldimg,EtalonHist) 
               Cloud = pp.resample(Cloud)               
               Cloud.normalise(oldimg,EtalonHist)          
               
           else:
               Cloud = pp.drift(Cloud)
               Cloud.normalise(oldimg,EtalonHist) 
               Cloud = pp.resample(Cloud)   
               Cloud.meanshift(oldoldimg,oldimg)               
               Cloud.normalise(oldimg,EtalonHist) 
              
           
           oldoldimg = np.copy(oldimg)
           print('##########'+str(count))
           
           showimg = np.copy(oldimg)
           print(Cloud.quantil)
           for i in Cloud:
#               ListOfHist = pp.CalculateHist(oldimg,i.y,i.x)
#               ####################################                             
#               color = ('b','g','r')
#               for var,col in enumerate(color):
#                   plt.plot(ListOfHist[var],color = col)
#                   plt.xlim([0,256])
#                   
#               
#               ######################################
#               plt.show()
              # print (i.x  ,  i.y  , i.w ,  i.c,  oldimg[i.y,i.x,:] )
               #if i.w <=0.09:
               cv2.circle(showimg,(i.x, i.y), 1, (0,255,0), -1)
               #else:
               #cv2.circle(showimg,(i.x, i.y), 1, (255,0,0), -1)
           
           
           cv2.imshow('frame',showimg)
       else:
           cv2.imshow('frame',img)
       
       
       c = cv2.waitKey(0)                   
       plt.close()
       if c == 27:
          break
       oldimg = np.copy(img)
       
cv2.destroyAllWindows()

















