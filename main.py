import time
import pynput
import random
from keys import forward, left, reverse, right
from controller.controller import Controller

PI = 3.14
PI2 = 1.57
NON_IMPACTING = 0.314

controller = pynput.keyboard.Controller()
wheelController = Controller()
# -------- Main Program Loop -----------
time.sleep(5)
while True:
    # --- Getting angles from the controller
    roll, pitch, yaw = wheelController.getRotations()
    # --- Transforming retrieved angles into pressing buttons
    if 0 < roll < PI2:
        forw = PI2 - roll
        if -PI2 < yaw < 0:
            if random.random() < (forw / (abs(forw) + abs(yaw))):
                forward(controller)
            else:
                left(controller)
        elif 0 < yaw < PI2:
            if random.random() < (forw / (abs(forw) + abs(yaw))):
                forward(controller)
            else:
                right(controller)
        # else:
        #     forward(controller)
    elif PI2 < roll < PI:
        rev = roll - PI2
        if -PI2 < yaw < 0:
            if random.random() < (rev / (abs(rev) + abs(yaw))):
                reverse(controller)
            else:
                left(controller)
        elif 0 < yaw < PI2:
            if random.random() < (rev / (abs(rev) + abs(yaw))):
                reverse(controller)
            else:
                right(controller)