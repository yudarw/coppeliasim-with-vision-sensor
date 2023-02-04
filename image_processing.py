# Example of read image data from CoppeliaSim

import cv2 as cv
import numpy as np
import sim
import time

# ============================================================= #
#  Color Image Filtering :
# ============================================================= #
def filter_image(img, filterColor):

    if filterColor == 'red':
        lower_bound = np.array([0, 70, 50])
        upper_bound = np.array([10, 255, 255])
    elif filterColor == 'green':
        lower_bound = np.array([36, 25, 25])
        upper_bound = np.array([70, 255, 255])
    elif filterColor == 'blue':
        lower_bound = np.array([105, 70, 50])
        upper_bound = np.array([130, 255, 255])

    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Create a mask using the bounds set
    mask = cv.inRange(hsv, lower_bound, upper_bound)
    # Create an inverse of the mask
    mask_inv = cv.bitwise_not(mask)
    # Filter only the red colour from the original image using the mask (foreground)
    res = cv.bitwise_and(img, img, mask=mask)
    # Filter the regions containing colours other than red from the grayscale image
    background = cv.bitwise_and(gray, gray, mask=mask_inv)
    # Convert the one channelled grayscale background to a three channelled image
    background = np.stack((background,) * 3, axis=-1)
    # add the foreground and the background
    added_img = cv.add(res, background)

    return mask, mask_inv, res, added_img, hsv

# ============================================================= #
#  Orientation Detection :
# ============================================================= #
def detect_orientation(img):
    # Convert image to grayscale:
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Convert image to binary:
    ret, bw = cv.threshold(gray, 50, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    contours, res = cv.findContours(bw, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

    for i, c in enumerate(contours):

        # Calculate the area of each contour
        area = cv.contourArea(c)

        # Ignore contours that are too small or too large
        #if area < 3700 or 100000 < area:
        #    continue

        # cv.minAreaRect returns:
        # (center(x, y), (width, height), angle of rotation) = cv2.minAreaRect(c)
        rect = cv.minAreaRect(c)
        box = cv.boxPoints(rect)
        box = np.int0(box)

        # Retrieve the key parameters of the rotated bounding box
        center = (int(rect[0][0]), int(rect[0][1]))
        width = int(rect[1][0])
        height = int(rect[1][1])
        angle = int(rect[2])

        if width < height:
            angle = 90 - angle
        else:
            angle = -angle

        #label = "(" + str(angle) + " deg"

        label = "({x}, {y}, Angle={ori})".format(x=center[0], y=center[1], ori=angle)

        #textbox = cv.rectangle(img, (center[0] - 35, center[1] - 25),
        #                       (center[0] + 295, center[1] + 10), (255, 255, 255), -1)

        cv.putText(img, label, (center[0], center[1]),
                   cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1, cv.LINE_AA)

        cv.drawContours(img, [box], 0, (0, 0, 255), 2)

    cv.imshow('Output Image', img)

    return img


sim.simxFinish(-1)
clientId = sim.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
sim.simxStartSimulation(clientId, sim.simx_opmode_blocking)

if clientId != -1:
    # Get vision sensor handle
    ret, visionHandle = sim.simxGetObjectHandle(clientId, '/Vision_sensor', sim.simx_opmode_oneshot_wait)
    # Start streaming image data
    ret, resolution, image = sim.simxGetVisionSensorImage(clientId, visionHandle, 0, sim.simx_opmode_streaming)

    time.sleep(1)
    ret, resolution, image = sim.simxGetVisionSensorImage(clientId, visionHandle, 0, sim.simx_opmode_buffer)
    if ret == sim.simx_return_ok:
        img = np.array(image, dtype=np.uint8)
        img.resize([resolution[1], resolution[0], 3])
        img2 = cv.cvtColor(img, cv.COLOR_RGB2BGR)
        img2 = cv.flip(img2, 0)
        #a,b,c,d,e= filter_image(img2, 'green')
        a = detect_orientation(img2)


    elif ret == sim.simx_return_novalue_flag:
        print('No image yet')
        pass

    if cv.waitKey(0):
        cv.destroyAllWindows()