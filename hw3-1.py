import numpy as np
import cv2 as cv
img = cv.imread('einsteinSample.jpg')
mask = cv.imread('einsteinMask.jpg',0)
dst = cv.inpaint(img,mask,3,cv.INPAINT_TELEA)
cv.imwrite("result2.jpg",dst)