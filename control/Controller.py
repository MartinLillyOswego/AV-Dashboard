# Imports
import threading

try:
    import pygame
    from pygame.locals import KMOD_CTRL
    from pygame.locals import KMOD_SHIFT
    from pygame.locals import K_0
    from pygame.locals import K_9
    from pygame.locals import K_BACKQUOTE
    from pygame.locals import K_BACKSPACE
    from pygame.locals import K_COMMA
    from pygame.locals import K_DOWN
    from pygame.locals import K_ESCAPE
    from pygame.locals import K_F1
    from pygame.locals import K_LEFT
    from pygame.locals import K_PERIOD
    from pygame.locals import K_RIGHT
    from pygame.locals import K_SLASH
    from pygame.locals import K_SPACE
    from pygame.locals import K_TAB
    from pygame.locals import K_UP
    from pygame.locals import K_a
    from pygame.locals import K_b
    from pygame.locals import K_c
    from pygame.locals import K_d
    from pygame.locals import K_f
    from pygame.locals import K_g
    from pygame.locals import K_h
    from pygame.locals import K_i
    from pygame.locals import K_l
    from pygame.locals import K_m
    from pygame.locals import K_n
    from pygame.locals import K_o
    from pygame.locals import K_p
    from pygame.locals import K_q
    from pygame.locals import K_r
    from pygame.locals import K_s
    from pygame.locals import K_t
    from pygame.locals import K_v
    from pygame.locals import K_w
    from pygame.locals import K_x
    from pygame.locals import K_z
    from pygame.locals import K_MINUS
    from pygame.locals import K_EQUALS
except ImportError:
    raise RuntimeError('cannot import pygame, make sure pygame package is installed')

class Controller(threading.Thread):
    def __init__(self, vehicle):
        # Variables
        super(Controller, self).__init__()
        self.vehicle = vehicle
        pygame.init()

    def controllerConnect(self):
        # Initialize pygame and joystick
        pygame.init()
        pygame.joystick.init()

        # clear terminal window
        # self.clearWindow()

        # Get number of controllers
        self.controllerCount = pygame.joystick.get_count()
        if self.controllerCount > 0:
            self.vehicle.controller = pygame.joystick.Joystick(0)
            self.vehicle.controllerName = self.vehicle.controller.get_name()
            self.vehicle.connected = True
            print(f"{self.vehicle.controllerName}")
        else:
            #print(f"No Controller Connected")
            self.vehicle.connected = False
            self.vehicle.controllerName = None
            self.vehicle.controller = None
        # time.sleep(2)

    '''
    def clearWindow(self):
        os.system("cls")
        print("\033[H\033[J", end="")
    '''

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # nothing yet
                pass
            if event.type == pygame.JOYDEVICEADDED or event.type == pygame.JOYDEVICEREMOVED:
                self.controllerConnect()
            if event.type == pygame.JOYBUTTONDOWN:
                # handbrake
                if self.controller.get_button(0) == 1:
                    if self.vehicle.handbrakeToSend == 0:
                        self.vehicle.handbrakeToSend = 255
                    else:
                        self.vehicle.handbrakeToSend = 0

                # gear selection
                if self.vehicle.gear[-1] == 1 and self.vehicle.speed[-1] >= 10:
                    self.vehicle.gearToSend = min(5, self.vehicle.gear + self.vehicle.controller.get_button(5))
                elif self.vehicle.gear[-1] == 1 and self.vehicle.speed[-1] < 10:
                    self.vehicle.gearToSend = min(5, self.vehicle.gear + self.vehicle.controller.get_button(5))
                    self.vehicle.gearToSend = max(0, self.vehicle.gear - self.vehicle.controller.get_button(4))
                    if self.controller.get_button(1) == 1:
                        self.vehicle.gearToSend = 0
                else:
                    self.vehicle.gearToSend = min(5, self.vehicle.gear + self.vehicle.controller.get_button(5))
                    self.vehicle.gearToSend = max(0, self.vehicle.gear - self.vehicle.controller.get_button(4))

            if event.type == pygame.JOYAXISMOTION:
                self.vehicle.throttleToSend = int(((self.vehicle.controller.get_axis(5) + 1) * 255) / 2)
                self.vehicle.brakeToSend = int(((self.vehicle.controller.get_axis(4) + 1) * 255) / 2)
                self.vehicle.steering_angleToSend = int(((self.vehicle.controller.get_axis(0) + 1) * 255) / 2)

            print(f"{self.vehicle.throttleToSend}")
            print(f"{self.vehicle.brakeToSend}")
            print(f"{self.vehicle.steering_angleToSend}")
    # Handles different controller inputs
    def GetControllerValue(self, selection):
        if self.controller_name == "Xbox One for Windows" | "Logitech G HUB G920 Driving Force Racing Wheel USB":
            buttons = {
                "A": 0,
                "B": 1,
                "X": 2,
                "Y": 3,
                "LeftBumper": 4,
                "RightBumper": 5,
                "LeftJoyIn": 6,
                "RightJoyIn": 7,
                "View": 8,
                "Menu": 9,
                "Home": 10
            }

            axis = {
                "LeftJoyPan": 0,
                "LeftJoyTilt": 1,
                "RightJoyPan": 2,
                "RightJoyTilt": 3,
                "LeftTrigger": 4,
                "RightTrigger": 5
            }

            pads = {
                "Left": 2,
                "Right": 1,
                "Up": 0,
                "Down": 3
            }

    # elif self.controller_name == "Logitech G HUB G920 Driving Force Racing Wheel USB"
    def GetKeyboardValue(self, selection):
        keys = {
            "Throttle": K_w,
            "Brake": K_b,
            "SteerLeft": K_a,
            "SteerRight": K_d,
            "Reverse": K_q,
            "ManualMode": K_m,
            "GearUp": K_UP,
            "GearDown": K_DOWN,
            "Menu": K_h,
            "Select": K_b,
            "Options": K_o,
        }

    def run(self):
        while True:
            self.get_events()
            if self.vehicle.exit:
                break
