from coppeliasim import CoppeliaSim, CoppeliaArmRobot
import time
import sim

msim = CoppeliaSim()
clientID = msim.connect(19997)
robot = CoppeliaArmRobot('UR10')

time.sleep(1)

if clientID != -1:
    pos = robot.readPosition()
    print(pos)

    newpos = pos
    newpos[0] = newpos[0] + 100

    robot.setPosition(newpos)

    time.sleep(5)
    msim.stopSimulation()