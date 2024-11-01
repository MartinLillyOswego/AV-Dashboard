
#Imports
import pygame
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
		self.controller
		self.controller_name
		self.number_controllers
		self.IsConnected

	#def SelectControllerType(self, controller):
	def IsControllerConnected()
		if pygame.joystick.get_count() < 1:
			print("Controller Not Connected")
			self.IsConnected = False
		else:
			self.controller = pygame.joystick.Joystick(0)
			self.controller.init()
			self.IsConnected = True
			self.controller_name = self.controller.get_name()
			print(f"Controller Name: {self.controller.get_name()}")
			if pygame.joystick.get_count() > 1:
				print("One controller allowed at any time")


	#Handles different controller inputs
	def GetControllerValue(selection):	
		if self.controller_name == "Xbox One for Windows"
			buttons = {
				"Reverse"   :self.controller.get_button(1),
				"GearUp"    :self.controller.get_button(5),
				"GearDown"  :self.controller.get_button(4),
				"ManualMode":self.controller.get_button(2),
				"Menu"      :self.controller.get_button(7),
				"Options"   :self.controller.get_button(6),
				"Home"      :self.controller.get_button(10),
				"Select"    :self.controller.get_button(0),
				"Back"      :self.controller.get_button(1)
			}

			axis = {
				"Throttle" :self.controller.get_axis(6),
				"Brake"    :self.controller.get_axis(5),
				"Steering" :self.controller.get_axis(0)	
			}

			pads = {
				"Left"  :self.controller.get_hats(2),
				"Right" :self.controller.get_hats(1),
				"Up"    :self.controller.get_hats(0),
				"Down"  :self.controller.get_hats(3)
			}

		'''
		elif self.controller_name == "Logitech G29 for Windows"

		'''

	def GetKeyboardValue():

		keys = {
			"Throttle": key_w,
			"Brake": key_b,
			"SteerLeft": 


		}

	#main loop	
	def GameLoop():

