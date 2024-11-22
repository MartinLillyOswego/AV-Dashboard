from manual_control import CarlaThread
from Vehicle import Vehicle
from manual_control import CommunicationMC

ogv = Vehicle()
icv = Vehicle()

c = CommunicationMC(vehicle=icv, carlaData=ogv)
c.start()

ct = CarlaThread(outgoing_vehicle=ogv, incoming_vehicle=icv)
ct.start()