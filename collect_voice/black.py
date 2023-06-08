# import required libraries
import cv2
import numpy as np

# create a black image
img = np.zeros((1920, 1080, 3), dtype = np.uint8)

# display the image using opencv
cv2.imshow('black image', img)
cv2.waitKey(0)