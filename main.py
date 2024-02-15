import sim
import cv2 as cv
import numpy as np
import time
import array
from PIL import Image
from coppeliasim import CoppeliaSim, CoppeliaSensor
from coppeliasim import Conveyor
import matplotlib.pyplot as plt



if __name__ == '__main__':
    mSim = CoppeliaSim()
    mSim.connect(19997)
    sensor = CoppeliaSensor("Proximity_sensor","Proximity")
    conveyor = Conveyor("ConveyorSim")
    conveyor.setSpeed(0.1)
    
    while sim.simxGetConnectionId(mSim.clientId != -1):
        res, dist = sensor.getProximityStatus()
        if dist == True:
            conveyor.setSpeed(0)
        time.sleep(0.1)