from threading import Thread
import threading
import time

def start_dashboard():

    # load config, import dependencies
    import control.config as dashboard_config
    dashboard_config.read(dashboard_config.CONFIG_FILE)
    try:
        from communication.Communication import Communication
        from control.Vehicle import Vehicle
        from python_gui.gui import GUI
        from control.Controller import Controller
        from control.ErrorChecks import ErrorChecks
    except ImportError:
        raise RuntimeError("cannot import local dependencies")

    # create instance of Vehicle class
    telemetry = Vehicle()

    # start a thread for the controller
    controller_thread = Controller(vehicle=telemetry)
    controller_thread.start()

    # start the communication thread
    communication_thread = Communication(vehicle=telemetry)
    communication_thread.start()
    time.sleep(1)

    # start the gui thread
    gui_thread = GUI(vehicle=telemetry)
    gui_thread.start()
    
    # error detection thread
    error_thread = ErrorChecks(vehicle=telemetry)
    error_thread.start()

start_dashboard()
