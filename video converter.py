


import numpy as np
import cv2
import os


def render(img_rgb):

    img_rgb = cv2.resize(img_rgb, (500,500))
    numDownSamples = 2       # number of downscaling steps
    numBilateralFilters = 50  # number of bilateral filtering steps

    # -- STEP 1 --
    # downsample image using Gaussian pyramid
    img_color = img_rgb
    for _ in xrange(numDownSamples):
        img_color = cv2.pyrDown(img_color)
    #cv2.imshow("downcolor",img_color)
    #cv2.waitKey(0)
    # repeatedly apply small bilateral filter instead of applying
    # one large filter
    for _ in xrange(numBilateralFilters):
        img_color = cv2.bilateralFilter(img_color, 9, 9, 7)
    #cv2.imshow("bilateral filter",img_color)
    #cv2.waitKey(0)
    # upsample image to original size
    for _ in xrange(numDownSamples):
        img_color = cv2.pyrUp(img_color)
    #cv2.imshow("upscaling",img_color)
    #cv2.waitKey(0)
    # -- STEPS 2 and 3 --
    # convert to grayscale and apply median blur
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    img_blur = cv2.medianBlur(img_gray, 3)
    #cv2.imshow("grayscale+median blur",img_color)
    #cv2.waitKey(0)
    # -- STEP 4 --
    # detect and enhance edges
    img_edge = cv2.adaptiveThreshold(img_blur, 255,
                                     cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY, 9, 2)
    #cv2.imshow("edge",img_edge)
    #cv2.waitKey(0)

    # -- STEP 5 --
    # convert back to color so that it can be bit-ANDed with color image
    (x,y,z) = img_color.shape
    img_edge = cv2.resize(img_edge,(y,x))
    img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
    #cv2.imwrite("edge.png",img_edge)
    #cv2.imshow("step 5", img_edge)
    #cv2.waitKey(0)
    #img_edge = cv2.resize(img_edge,(i for i in img_color.shape[:2]))
    #print img_edge.shape, img_color.shape
    return cv2.bitwise_and(img_color, img_edge)



FILE_OUTPUT = 'output.avi'

# Checks and deletes the output file
# You cant have a existing file or it will through an error
if os.path.isfile(FILE_OUTPUT):
    os.remove(FILE_OUTPUT)


cap = cv2.VideoCapture("pp2.avi")
while not cap.isOpened():
    cap = cv2.VideoCapture("pp2.mp4")
    cv2.waitKey(1000)
    print ("Wait for the header")

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',-1, 20.0, (640,480))

pos_frame = cap.get(1)
while True:

    flag, frame = cap.read()

    if flag:
        # The frame is ready and already captured
        frame = render (frame)
        cv2.imshow('video', frame)
        out.write(frame)
        pos_frame = cap.get(1)
        print (str(pos_frame)+" frames")


    else:
        # The next frame is not ready, so we try to read it again
        cap.set(1, pos_frame-1)
        print ("frame is not ready")
        # It is better to wait for a while for the next frame to be ready
        cv2.waitKey(1000)

    if cv2.waitKey(10) == 27:
        break

    if cap.get(1) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        # If the number of captured frames is equal to the total number of frames,
        # we stop
        break

cap.release()
out.release()
cv2.destroyAllWindows()