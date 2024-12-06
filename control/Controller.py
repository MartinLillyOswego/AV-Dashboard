from inputs import get_gamepad, devices
import time
import threading

class Controller(threading.Thread):
    def __init__(self, vehicle):
        super(Controller, self).__init__()
        self.vehicle = vehicle

    def keyboard_connect(self):
        # Check for keyboards
        keyboards = devices.keyboards

        # Get length of keyboards
        index = len(keyboards)
        #print(f"{keyboards[0]}")

        # If no keyboards connected
        if not keyboards:
            self.vehicle.keyboard_name = None
            self.vehicle.keyboard_reference = None
            self.vehicle.keyboard_connected = False

        # Else keyboards connected
        else:
            # Select first keyboard
            keyboard = keyboards[index - 1]
            # check if still active
            try:

                # Try to pull data from keyboard
                working = keyboard.get_key()

                # Keyboard still connected
                self.vehicle.keyboard_name = keyboard.name
                self.vehicle.keyboard_reference = keyboard
                self.vehicle.keyboard_connected = True

            # Except if unable to pull data from keyboard
            except Exception as error:

                # Keyboard is no longer active
                self.vehicle.keyboard_name = None
                self.vehicle.keyboard_reference = None
                self.vehicle.keyboard_connected = False



    def controller_connect(self):
        # Check for controllers
        devices._detect_gamepads()
        controllers = devices.gamepads

        # Find length and choose last controller on list
        index = len(controllers)

        # If no controllers connected
        if not controllers:
            self.vehicle.controller_name = None
            self.vehicle.controller_reference = None
            self.vehicle.controller_connected = False

        # Else controllers connected, select latest one
        else:
            controller = controllers[index - 1]

            # check if still active
            try:

                # Try to pull data from controller
                working = controller.read()

                # Controller still connected
                self.vehicle.controller_name = controller.name
                self.vehicle.controller_reference = controller
                self.vehicle.controller_connected = True

            # Except if unable to pull data from controller
            except Exception as error:

                # Controller is no longer active
                self.vehicle.controller_name = None
                self.vehicle.controller_reference = None
                self.vehicle.controller_connected = False


    def get_events(self):

        while True:
            # Check for devices
            if self.vehicle.controller_connected:

                # Try to read from controller
                try:
                    # Get controller inputs
                    controller_events = self.vehicle.controller_reference.read()
                    for event in controller_events:

                        # Get latest index of vehicle class and controller name
                        ind = len(self.vehicle.speed)
                        controller = self.vehicle.controller_name

                        # if button pressed on gamepad
                        if event.ev_type == 'Key':

                            # Shift up
                            if event.code == self.get_input(controller,"ShiftUp") and event.state == 1:
                                # If in reverse must be below 5mph
                                if self.vehicle.speed[-1] < 10 and self.vehicle.gear[-1] == 0:
                                    # Shift up
                                    self.vehicle.gearToSend = 1
                                # Else if not in reverse
                                elif self.vehicle.gear[-1] != 0:
                                    #Shift up
                                    self.vehicle.gearToSend = min(5, self.vehicle.gear[-1] + 1)

                            # Shift down
                            if event.code == self.get_input(controller,"ShiftDown") and event.state == 1:
                                # If in neutral must be below 5mph
                                if self.vehicle.speed[-1] < 5 and self.vehicle.gear[-1] == 1:
                                    # Shift down
                                    self.vehicle.gearToSend = 0
                                # Else if not in neutral
                                elif self.vehicle.gear[-1] != 1:
                                    #Shift down
                                    self.vehicle.gearToSend = max(0, self.vehicle.gear[-1] - 1)

                            # Handbrake
                            if event.code == self.get_input(controller, "Handbrake") and event.state == 1:
                                # Apply handbrake
                                self.vehicle.emergency_brakeToSend = 255
                            else:
                                self.vehicle.emergency_brakeToSend = 0


                        # Else if event is a joystick
                        if event.ev_type == 'Absolute':

                            # Steering
                            if event.code == self.get_input(controller, "Steer"):
                                steering_angle = int((event.state + 32768) * (255/65535))       # Map from -32768_32768 to 0_255
                                self.vehicle.steering_angleToSend = steering_angle

                            # Brake
                            elif event.code == self.get_input(controller, "Brake"):
                                brake = event.state
                                self.vehicle.brakeToSend = brake

                            # Throttle
                            elif event.code == self.get_input(controller, "Throttle"):
                                throttle = event.state
                                self.vehicle.throttleToSend = throttle

                # Except error for reading controller and reconnect
                except Exception as error:
                    self.controller_connect()

            # Else connect to controller
            else:
                self.controller_connect()
            '''
            # Check for keyboard
            if self.vehicle.keyboard_connected:
                # Try to read from keyboard
                try:
                    # Get keyboard inputs
                    keyboard_events = self.vehicle.keyboard_reference.get_key()
                    for event in keyboard_events:
                        print(f"{event.ev_type}, {event.code}, {event.state}")

                # Except error for reading keyboard and reconnect
                except Exception as error:
                    self.keyboard_connect()
            else:
                self.keyboard_connect()
            '''

    @staticmethod
    def get_input(controller_name, input_selection):
        # Xbox One controller
        xbox_one = {
            "Throttle"  : "ABS_RZ",    # Right trigger
            "Brake"     : "ABS_Z",      # Left trigger
            "Handbrake" : "BTN_SOUTH",  # A button
            "Steer"     : "ABS_X",      # Left Joystick
            "ShiftDown" : "BTN_TL",     # Left bumper
            "ShiftUp"   : "BTN_TR",     # Right bumper
            "Select"    : "BTN_MENU",   # Left select
            "Menu"      : "BTN_SELECT", # Right menu
            "D_L/R"     : "ABS_HAT0X",  # Dpad left and right -1 for left 1 for right
            "D_U/D"     : "ABS_HAT0Y",  # Dpad up and down -1 for up 1 for down
        }
        # Check for type of connected controller
        if controller_name == "Microsoft X-Box 360 pad":
            return xbox_one.get(input_selection)


    def run(self):
        while True:
            time.sleep(2)   #Wait for program to start
            self.get_events()
            if self.vehicle.exit:
                break
