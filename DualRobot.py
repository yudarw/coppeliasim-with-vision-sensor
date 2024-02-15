import sim
import cv2 as cv
import numpy as np
import time
import array
from PIL import Image
from coppeliasim import CoppeliaSim, CoppeliaSensor, CoppeliaArmRobot
from coppeliasim import Conveyor
import matplotlib.pyplot as plt
import threading


def motion1():
    mRobot = CoppeliaArmRobot("UR10")
    time.sleep(3)
    pos = mRobot.readPosition()
    
    pos1 = [550, 172, 0, -180, 0, 90] 
    pos2 = [550, 172, 300, -180, 0, 90]

    while True:
        mRobot.setPosition(pos1)
        time.sleep(3)
        mRobot.setPosition(pos2)
        time.sleep(3)

def motion2():
    mRobot = CoppeliaArmRobot("UR10_1")
    time.sleep(3)
    pos = mRobot.readPosition()
    print(pos)
    while True:
        pos[1] += 350
        mRobot.setPosition(pos)
        time.sleep(3)

        pos[1] -= 350
        mRobot.setPosition(pos)
        time.sleep(3)

def main():
    # Connect Coppeliasim
    mSim = CoppeliaSim()
    mSim.connect(19997)

  

    threadRobot1 = threading.Thread(target=motion1)
    threadRobot1.start()

    #threadRobot2 = threading.Thread(target=motion2)
    #threadRobot2.start()

    #threadRobot1.join()
    #threadRobot2.join()

if __name__ == '__main__':
    main()
    