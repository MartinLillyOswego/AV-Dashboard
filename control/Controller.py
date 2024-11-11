
#Imports
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
    #from pygame.locals import K_ENTER
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
		pygame.init()

	def get_vehicle_commands(self, packet):
		#try to connect with latest controller
		if pygame.joystick.get_count()>0:
			self.controller = pygame.joystick.Joystick(0)
			self.controller_name = self.controller.get_name()

		#Call get events method
		self.get_events(packet)

		return packet

	def get_events(self, packet):
		#Look for any events
		for event in pygame.event.get():
			if event.type == pygame.JOYBUTTONDOWN:
				#Find the pressed button
				if self.controller.get_button() == 0:
					#Gear Down / Might need to be mapped to 0-255 instead of 0,1,2
					if packet[9] == 1:		#If in neutral
						if packet[9] <= 5:	#Reverse lockout
							packet[9] += - 1
					elif packet[9] > 0:
						packet[9] += - 1
				
				if self.controller.get_button() == 3:
					#Gear Up / Might need to be mapped to 0-255 instead of 0,1,2
					if packet[9] == 0:		#If in reverse
						if packet[9] <= 5:	#Reverse lock
							packet[9] += 1
					elif packet[9] < 4:
						packet[9] += 1

			#elif event.type == pygame.JOYAXISMOTION:
				#Get all axis values
			self.throttle = self.controller.get_axis(5)
				#print (f"THROTTLE{type(self.throttle)}")
			self.brake = self.controller.get_axis(4)
			self.steering = self.controller.get_axis(0)

				#Map axis
			self.throttle = ((self.throttle + 1)/2) * 255
			self.brake = ((self.brake + 1)/2) * 255
			self.steering = ((self.steering + 0.7)/1.4) * 255
				#print(f"{self.throttle}")

				#Change packet values
			packet[4] = int(self.throttle)
			packet[5] = int(self.brake)
			packet[7] = int(self.steering)

			#elif event.type == pygame.KEYUP:
				#if event.key == GetKeyboardValue(keys["Throttle"]):

		return packet

	#Handles different controller inputs
	def GetControllerValue(self, selection):	
		if self.controller_name == "Xbox One for Windows" | "Logitech G HUB G920 Driving Force Racing Wheel USB":
			buttons = {
				"A"           :0,
				"B"           :1,
				"X"           :2,
				"Y"           :3,
				"LeftBumper"  :4,
				"RightBumper" :5,
				"LeftJoyIn"   :6,
				"RightJoyIn"  :7,
				"View"        :8,
				"Menu"        :9,
				"Home"        :10
			}

			axis = {
				"LeftJoyPan"   :0,
				"LeftJoyTilt"  :1,
				"RightJoyPan"  :2,
				"RightJoyTilt" :3,
				"LeftTrigger"  :4,
				"RightTrigger" :5	
			}

			pads = {
				"Left"  :2,
				"Right" :1,
				"Up"    :0,
				"Down"  :3
			}

	'''
	elif self.controller_name == "Logitech G HUB G920 Driving Force Racing Wheel USB"
	'''
	def GetKeyboardValue(self, selection):

		keys = {
			"Throttle"   :K_w,
			"Brake"      :K_b,
			"SteerLeft"  :K_a,
			"SteerRight" :K_d,
			"Reverse"    :K_q,
			"ManualMode" :K_m,
			"GearUp"     :K_UP,
			"GearDown"   :K_DOWN,
			"Menu"       :K_h,
			"Select"	 :K_b,
			"Options"    :K_o,
		}
