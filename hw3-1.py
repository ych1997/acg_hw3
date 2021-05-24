import numpy as np
import cv2 as cv
img = cv.imread('1.png')
mask = cv.imread('1.png',0)
dst = cv.inpaint(img,mask,3,cv.INPAINT_TELEA)
cv.imwrite('1_result.jpg',dst)