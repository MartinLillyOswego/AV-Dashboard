from threading import Thread
import threading
import signal
import time

def start_dashboard():
    # load config, import dependencies
    import control.config as dashboard_config
    dashboard_config.read(dashboard_config.CONFIG_FILE)
    try:
        from communication.Communication import Communication
        from control.Vehicle import Vehicle
        from python_gui.gui import GUI
    except ImportError:
        raise RuntimeError("cannot import local dependencies")

    # create instance of Vehicle class
    telemetry = Vehicle()

    # start the receiver thread
    communication_thread = Communication(vehicle=telemetry)
    communication_thread.start()

    time.sleep(1)
    # start the gui thread
    gui_thread = GUI(vehicle=telemetry)
    gui_thread.start()

# run
def run():
    import control.config as helper_config
    helper_config.read(helper_config.CONFIG_FILE)
    start_dashboard()

run()
