

import cv2
import numpy as np

num_down = 2       # number of downsampling steps
num_bilateral = 7  # number of bilateral filtering steps

image = cv2.imread('zermatt_cartoon.jpg')

img_color = image
for _ in xrange(num_down):
    img_color = cv2.pyrDown(img_color)

for _ in xrange(num_bilateral):
    img_color = cv2.bilateralFilter(img_color, d=9,
                                    sigmaColor=9,
                                    sigmaSpace=7)


for _ in xrange(num_down):
    img_color = cv2.pyrUp(img_color)


img_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
img_blur = cv2.medianBlur(img_gray, 7)

img_edge = cv2.adaptiveThreshold(img_blur, 255,
                                 cv2.ADAPTIVE_THRESH_MEAN_C,
                                 cv2.THRESH_BINARY,
                                 blockSize=9,
                                 C=2)

# convert back to color, bit-AND with color image
img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)

cv2.imshow( '1', img_color)
cv2.imshow( '2', img_edge)
img_cartoon = cv2.bitwise_and(img_color, img_edge)

# display
cv2.imshow("cartoon", img_cartoon)

cv2.waitKey(0)
cv2.destroyAllWindows()