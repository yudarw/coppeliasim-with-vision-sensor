import sim
import cv2 as cv
import numpy as np
import time
import array
from PIL import Image
from coppeliasim import CoppeliaSim, CoppeliaSensor
import matplotlib.pyplot as plt

mSim = CoppeliaSim()
mSim.connect(19997)
camera = CoppeliaSensor("Vision_sensor", 0)

time.sleep(2)

#es, image = camera.getImage()
#print(res)

#cap = cv.VideoCapture(0)

while sim.simxGetConnectionId(mSim.clientId != -1):
    ret, res, image = camera.getImage()    
    #if ret == sim.simx_return_ok:
    #    img = np.array(image, dtype=np.uint8)
    #    img.resize([res[1], res[0], 3])
    #    img2 = cv.cvtColor(img, cv.COLOR_RGB2BGR)
    #    img2 = cv.flip(img2, 0)
    #    cv.imshow("image", img2)    
    image_byte_array = array.array('b', image)
    im = Image.frombuffer("RGB",(res[0], res[1]), image_byte_array, "raw", "RGB", 0, 1)
    cv.imshow("image", im)

    #_, frame = cap.read()
    #cv.imshow('frame',frame)

    key = cv.waitKey(5) & 0xFF
    if key == 27:
        break

cv.destroyAllWindows()