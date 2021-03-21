import cv2
import numpy as np
import imutils

   
# Initializing the HOG person 
# detector 
hog = cv2.HOGDescriptor() 
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector()) 
   
# Reading the Image 
image = cv2.imread('img.png') 
   
# Resizing the Image 
image = imutils.resize(image, 
                       width=min(400, image.shape[1])) 
   
# Detecting all the regions in the  
# Image that has a pedestrians inside it 
(regions, _) = hog.detectMultiScale(image,  
                                    winStride=(4, 4), 
                                    padding=(4, 4), 
                                    scale=1.05) 
   
# Drawing the regions in the Image 
for (x, y, w, h) in regions: 
    cv2.rectangle(image, (x, y),  
                  (x + w, y + h),  
                  (0, 0, 255), 2) 
  
# Showing the output Image 
cv2.imshow("Image", image) 
cv2.waitKey(0) 
   
cv2.destroyAllWindows() 