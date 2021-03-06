import numpy as np
import cv2
 

def meanshift(particle,oldimg,newimg):

    r,h,c,w = particle.y-5,10,particle.x-5,10  # simply hardcoded the values
    track_window = (c,r,w,h)
 
 # set up the ROI for tracking
    roi = oldimg[r:r+h, c:c+w]
    hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
    roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
    cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
 
 # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
    term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

    hsv = cv2.cvtColor(newimg, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)
         # apply meanshift to get the new location
    ret, track_window = cv2.meanShift(dst, track_window, term_crit)
 
    return track_window


####################################

    