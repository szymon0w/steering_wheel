import time
from pynput import keyboard
import random
from keys import forward, left, reverse, right
from controller.controller import Controller

PI = 3.14
PI2 = 1.57
NON_IMPACTING = 0.314


class SteeringWheel():
    def __init__(self):
        self.stop = True
        self.controller = keyboard.Controller()
        self.listener = keyboard.Listener()
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
        self.wheelController = Controller()
    
    def on_press(self, key):
        if key == keyboard.Key.space:
            self.stop = not self.stop

    def on_release(self, key):
        pass
    def run_loop(self):
        # -------- Main Program Loop -----------
        while True:
            while self.stop:
                time.sleep(1)
                print('sleeping')
            print('running')
            # --- Getting angles from the controller
            roll, pitch, yaw = self.wheelController.getRotations()
            # --- Transforming retrieved angles into pressing buttons
            if 0 < roll < PI2:
                forw = PI2 - roll
                if -PI2 < yaw < 0:
                    if random.random() < (forw / (abs(forw) + abs(yaw))):
                        forward(self.controller)
                    else:
                        left(self.controller)
                elif 0 < yaw < PI2:
                    if random.random() < (forw / (abs(forw) + abs(yaw))):
                        forward(self.controller)
                    else:
                        right(self.controller)

            elif PI2 < roll < PI:
                rev = roll - PI2
                if -PI2 < yaw < 0:
                    if random.random() < (rev / (abs(rev) + abs(yaw))):
                        reverse(self.controller)
                    else:
                        left(self.controller)
                elif 0 < yaw < PI2:
                    if random.random() < (rev / (abs(rev) + abs(yaw))):
                        reverse(self.controller)
                    else:
                        right(self.controller)

if __name__ == '__main__':
    steering_wheel = SteeringWheel()
    steering_wheel.run_loop()


