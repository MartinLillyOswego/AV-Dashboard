import threading
#import Shutdown
import signal
import time

import control.config as config
config.read()
try:
    from control.ControlUnit import ControlUnit
    from communication.Receiver import Receiver
    from communication.Sender import Sender
    from control.Vehicle import Vehicle
    from python_gui.gui import GUI
except ImportError:
    raise RuntimeError("cannot import local dependencies")

# create instance of Vehicle class
telemetry = Vehicle()

# start the receiver thread
receiver_thread = Receiver(vehicle=telemetry)
receiver_thread.start()

# start the control unit
#control_unit = ControlUnit(vehicle=telemetry)
#control_unit.start()

# start the sender thread
sender_thread = Sender(vehicle=telemetry, receiver=receiver_thread, control_unit=None)
sender_thread.start()

time.sleep(3)
# start the gui thread
gui_thread = GUI(vehicle=telemetry)
gui_thread.start()


"""
def shutdown_signal(sig, frame):
    print("Shutdown signal received.")
    Shutdown.shutdown(receiver_thread, sender_thread, telemetry)

signal.signal(signal.SIGINT, shutdown_signal)
signal.signal(signal.SIGTERM, shutdown_signal)

try:
    while True:
        time.sleep(config.CARLA_SIM_DURATION)
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    shutdown_signal(None, None)
"""
