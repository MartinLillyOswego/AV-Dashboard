from threading import Thread
import threading
#import Shutdown
import signal
import time

def start_dashboard():
    # load config, import dependencies
    import control.config as dashboard_config
    dashboard_config.read(dashboard_config.CONFIG_FILE)
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

    # create the control unit
    control_unit = ControlUnit(vehicle=telemetry)

    # start the receiver thread
    receiver_thread = Receiver(vehicle=telemetry)
    receiver_thread.start()

    # start the sender thread
    sender_thread = Sender(vehicle=telemetry, receiver=receiver_thread, control_unit=control_unit)
    sender_thread.start()

    time.sleep(1)
    # start the gui thread
    gui_thread = GUI(vehicle=telemetry)
    gui_thread.start()

def start_carla_vehicle():
    # load config, import dependencies
    import control.config as emulated_config
    emulated_config.read(emulated_config.EMULATED_CONFIG_FILE)
    try:
        from control.ControlUnit import ControlUnit
        from communication.Receiver import Receiver
        from communication.Sender import Sender
        from control.Vehicle import Vehicle
        from python_gui.gui import GUI
        from control.manual_control_v0_9_12 import CarlaThread
    except ImportError:
        raise RuntimeError("cannot import local dependencies")

    # create shared instances of Vehicle class
    carla_vehicle_data = Vehicle()
    received_vehicle_commands = Vehicle()

    # start the vehicle emulator's receive thread
    r = Receiver(vehicle=received_vehicle_commands)
    r.start()

    # start the vehicle emulator's send thread
    s = Sender(vehicle=carla_vehicle_data, receiver=r, control_unit=None)
    s.start()

    # start the carla thread, which updates a shared instance of Vehicle
    ct = CarlaThread(outgoing_vehicle=carla_vehicle_data, incoming_vehicle=received_vehicle_commands)
    ct.start()

# run
def run():
    import control.config as helper_config
    helper_config.read(helper_config.CONFIG_FILE)
    if helper_config.USE_CARLA_DATA:
        #start_carla_vehicle()
        time.sleep(1)
    start_dashboard()

run()

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
