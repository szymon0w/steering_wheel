import time
import pynput
from keys import forward, left, reverse, right
from controller.controller import Controller

PI = 3.14
PI2 = 1.57
NON_IMPACTING = 0.314

# Loop until the user clicks the close button. 
# Used to manage how fast the screen updates
controller = pynput.keyboard.Controller()
wheelController = Controller()
# -------- Main Program Loop -----------
time.sleep(5)
while True:
    # --- Getting angles from the controller
    roll, pitch, yaw = wheelController.getRotations()
    # --- Transforming retrieved angles into pressing buttons
    if 0 < roll < PI2:
        if -PI2 < yaw < -NON_IMPACTING:
            left(controller)
        elif NON_IMPACTING < yaw < PI2:
            right(controller)
        else:
            forward(controller)
    elif PI2 < roll < PI:
        if -PI2 < yaw < -NON_IMPACTING:
            left(controller)
        elif NON_IMPACTING < yaw < PI2:
            right(controller)
        else:
            reverse(controller)