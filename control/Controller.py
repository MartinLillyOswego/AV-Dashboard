# Imports
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


class Controller:
    def __init__(self):
        # Variables
        self.connected = False
        self.controller = None
        self.controllerName = ""
        self.throttle = 0
        self.brake = 0
        self.steering = 128
        self.handbrake = 0
        self.gear = 1
        self.controllerCount = 0
        
    def controllerConnect(self):
        #Initialize pygame and joystick
        pygame.init()
        pygame.joystick.init()

        #clear terminal window
        #self.clearWindow()

        #Get number of controllers
        
        self.controllerCount = pygame.joystick.get_count()
        if self.controllerCount > 0:
            self.controller = pygame.joystick.Joystick(0)
            self.controllerName = self.controller.get_name()
            self.connected = True
            print(f"{self.controllerName}")
        else:
             print(f"No Controller Connected")
             self.connected = False
             self.controllerName = None
             self.controller = None
        #time.sleep(2)

    def get_vehicle_commands(self, packet):
        # try to connect with latest controller
        if not self.connected:
            self.controllerConnect()

        # Call get events method
        new_packet = self.get_events(packet)

        return new_packet

    '''
    def clearWindow(self):
        os.system("cls")
        print("\033[H\033[J", end="")
    '''
    


    def get_events(self, Packet):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #nothing yet
                pass
            if event.type == pygame.JOYBUTTONDOWN:
                if self.controller.get_button(0) == 1:
                    if self.handbrake == 0:
                        self.handbrake = 255
                    else:
                        self.handbrake = 0

                if self.gear == 1 and packet[0] >= 10:
                    self.gear = min(5, self.gear + self.controller.get_button(5))
                elif self.gear == 1 and packet[0] < 10:
                    self.gear = min(5, self.gear + self.controller.get_button(5))
                    self.gear = max(0, self.gear - self.controller.get_button(4))
                    if self.controller.get_button(1) == 1:
                        self.gear = 0
                else:
                    self.gear = min(5, self.gear + self.controller.get_button(5))
                    self.gear = max(0, self.gear - self.controller.get_button(4))

            if event.type == pygame.JOYAXISMOTION:
                self.throttle = int(((self.controller.get_axis(5)+1)*255)/2)
                self.brake    = int(((self.controller.get_axis(4)+1)*255)/2)
                self.steering = int(((self.controller.get_axis(0)+1)*255)/2)

            
            # Print screen
            #os.system("cls")
            #print("\033[H\033[J", end="")
            #print(f"Throttle   : {self.throttle}")
            #print(f"Brake      : {self.brake}")
            #print(f"Steer Angle: {self.steering}")
            #print(f"Hand Brake : {self.handbrake}")
            #print(f"Gear       : {self.gear}")
            #print(f"Controller :{self.controllerName}")
            #time.sleep(.1)
            
            # Assign packet 
            Packet[1] = self.throttle
            Packet[2] = self.brake
            Packet[5] = self.steering
        
        return Packet

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

    #elif self.controller_name == "Logitech G HUB G920 Driving Force Racing Wheel USB"
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
            "Select" :K_b,
            "Options": K_o,
        }
