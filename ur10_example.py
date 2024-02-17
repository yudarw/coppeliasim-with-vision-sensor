from coppeliasim import CoppeliaSim, CoppeliaArmRobot
import time
import sim
import numpy as np

def initialize_object():
    # Get object position:
    cuboid = np.zeros((9, 6))
    for i in range (9):
        cuboid[i] = robot.getObjectPosition(f"Cuboid{i-1}")
    print(cuboid)
    return cuboid

def initialize_targetPos():
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
    #time.sleep(1)
    #robot.suctionOFF()

    # Move Up:
    targetPos[2] = targetPos[2] + 50
    robot.setPosition2(targetPos)
    


def main():
    if clientID != -1:
        HomePos = robot.readPosition()
        pos = robot.readPosition()
        print("Current Robot Position: {}".format(pos))
        
        # Get Object Position
        objPos = robot.getObjectPosition("Cuboid")
        print("Object Position: {}".format(objPos))
        robot.suctionON()
        targetPos = pos
        targetPos[0] = objPos[0]
        targetPos[1] = objPos[1]
        targetPos[2] = objPos[2] + 50
        print("Target Position: {}".format(targetPos))
        robot.setPosition2(targetPos, True)

        targetPos[2] = objPos[2] + 30
        robot.setPosition2(targetPos, True)

        targetPos[2] = objPos[2] + 400
        robot.setPosition2(targetPos, True)

        robot.setSpeed(500, 90)
        endPos = robot.getObjectPosition("Dummy")
        targetPos[0] = endPos[0]
        targetPos[1] = endPos[1]
        targetPos[2] = endPos[2] + 100
        robot.setPosition2(targetPos, True)

        robot.setSpeed(10, 90)
        targetPos[2] = endPos[2] + 50
        robot.setPosition2(targetPos, True)
        robot.suctionOFF()
        #robot.suctionON()
        
        targetPos[2] = endPos[2] + 100
        robot.setPosition2(targetPos, True)

        robot.setSpeed(200, 90)
        robot.setPosition2(HomePos, True)
        
        
        time.sleep(2)
        msim.stopSimulation()


if __name__ == '__main__':
    msim = CoppeliaSim()
    clientID = msim.connect(19997)
    robot = CoppeliaArmRobot('UR10')
    time.sleep(1)    
    _object = initialize_object()
    _target = initialize_targetPos()
    
    for i in range(9):
        pos = _object[i]
        pickObject(pos)
        pos = _target[i]
        putObject(pos)

