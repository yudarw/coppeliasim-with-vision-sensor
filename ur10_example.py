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
    msim.stopSimulation()