import threading
import time
from Receiver import Receiver
from Vehicle import Vehicle
from Sender import Sender
import Shutdown
import signal

telemetry = Vehicle()
vehiclecommands = Vehicle()

receiverthread = Receiver(vehicle=vehiclecommands)
receiverthread.start()

senderthread = Sender(vehicle=telemetry, receiver=receiverthread, control_unit=None)
senderthread.start()

def shutdownsignal(sig, frame):
    print("Shutdown signal received.")
    Shutdown.shutdown(receiverthread, senderthread, telemetry)

signal.signal(signal.SIGINT, shutdownsignal)
signal.signal(signal.SIGTERM, shutdownsignal)

try:
    while True:
        time.sleep(1)
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    shutdownsignal(None, None)
