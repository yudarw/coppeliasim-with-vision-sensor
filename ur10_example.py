# ===================================================
# UR10 Pick and Place example
# 
# coppeliasim scene: pick_and_place.ttt
# ===================================================

from coppeliasim import CoppeliaSim, CoppeliaArmRobot
import time
import sim
import numpy as np

# Initialize object position:
def initialize_object():
    # Get object position:
    cuboid = np.zeros((9, 6))
    for i in range (9):
        objectName = f"Cuboid{i}"
        cuboid[i] = robot.getObjectPosition(objectName)
    print(cuboid)
    return cuboid

# Initialize target position:
def initialize_targetPos():
    # Get initial targat position in the simulation
    startPos  = robot.getObjectPosition("Target0")
    targetPos = np.zeros((9, 6))
    for i in range(9):
        targetPos[i] = startPos
    targetPos[1][0] += 100
    targetPos[2][0] += 200
    targetPos[3][1] -= 100
    targetPos[4][1] -= 100
    targetPos[4][0] += 100
    targetPos[5][1] -= 100
    targetPos[5][0] += 200
    targetPos[6][1] -= 200
    targetPos[7][1] -= 200
    targetPos[7][0] += 100
    targetPos[8][1] -= 200
    targetPos[8][0] += 200
    return targetPos

# Method for picking the object:
def pickObject(targetPos):
    currentPos = robot.readPosition()
    robot.suctionON()
    robot.setSpeed(300, 180) 
    # Move above the object
    targetPos[2] = targetPos[2] + 50
    targetPos[3] = currentPos[3]
    targetPos[4] = currentPos[4]
    targetPos[5] = currentPos[5]
    robot.setPosition2(targetPos)
    
    robot.setSpeed(50, 180)
    # Move down:
    targetPos[2] = targetPos[2] - 20
    robot.setPosition2(targetPos)
    
    #Move up:
    targetPos[2] = targetPos[2] + 100
    robot.setPosition2(targetPos)

# Method to put the object inside the box:
def putObject(targetPos):
    currentPos = robot.readPosition()

    # Move to position:
    robot.setSpeed(300, 180)
    targetPos[2] = targetPos[2] + 100
    targetPos[3] = currentPos[3]
    targetPos[4] = currentPos[4]
    targetPos[5] = currentPos[5]
    robot.setPosition2(targetPos)

    robot.setSpeed(10, 90)
    # Move Down:
    targetPos[2] = targetPos[2] - 40
    robot.setPosition2(targetPos)
    
    robot.suctionOFF()

    # Move Up:
    targetPos[2] = targetPos[2] + 50
    robot.setPosition2(targetPos)
    

if __name__ == '__main__':
    msim        = CoppeliaSim()
    clientID    = msim.connect(19997)
    robot       = CoppeliaArmRobot('UR10')
    time.sleep(3)    

    if clientID != -1:
        _object = initialize_object()
        _target = initialize_targetPos()

        # Do the pick and place of 9 objects        
        for i in range(9):
            pos = _object[i]
            print("TargetPos: {}".format(pos))
            pickObject(pos)
            pos = _target[i]
            putObject(pos)

