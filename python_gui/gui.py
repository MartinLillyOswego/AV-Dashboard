from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
import control.config as config
import threading
import uvicorn
import math
import os
from os import listdir
from os.path import isfile, join
import random
import logging

class GUI(threading.Thread):

    def __init__(self, vehicle):
        super(GUI, self).__init__()
        app = FastAPI()
        self.vehicle = vehicle
        self.responce_text = ""
        app.mount("/static", StaticFiles(directory="python_gui/static"), name="static")

        @app.get("/", response_class=HTMLResponse)
        async def read_index():
            with open("python_gui/dashboard.html", 'r') as f:
                return HTMLResponse(content=f.read())

        @app.get("/open_config", response_class=HTMLResponse)
        async def open_config(serial_port: str = "", max_speed: str = "", carla_state: str = ""):

            # enable carla
            if carla_state != "":
                config.USE_CARLA_DATA = not config.USE_CARLA_DATA
                self.responce_text = "Restart Required"
                config.write()

            # update serial port
            if serial_port != "":
                print(f"{config.get_time()}: Updating value for serial_port")
                config.CARLA_SERIAL_PORT = serial_port
                config.VEHICLE_PORT = serial_port
                self.responce_text = "Updated Serial Port, you may need to restart the dashboard"
                config.write()

            # updated allowed max speed
            if max_speed != "":
                try:
                    config.MAX_SPEED = float(max_speed)
                    self.responce_text = "Updated Allowed Max Speed"
                    config.write()
                except ValueError:
                    self.responce_text = "Invalid input for this filed"

            with open("python_gui/tuning_menu.html", 'r') as f:
                return HTMLResponse(content=f.read())

        @app.get("/config_data")
        async def get_config_data():
            carla_state = "Enable"
            if config.USE_CARLA_DATA:
                carla_state = "Disable"
            out = {
                "serial_port": config.VEHICLE_PORT,
                "max_speed": config.MAX_SPEED,
                "carla_state": carla_state,
                "responce_text": self.responce_text
            }
            self.responce_text = ""
            return out

        @app.get("/data")
        async def get_data():
            if len(vehicle.velocity) == 0:
                return {"speed": 0,
                        "throttle": 0,
                        "brake": 0,
                        "steering_angle": 0,
                        "battery_img": "static/icons/battery4.png",
                        "con_png": "static/icons/radio.png",
                        "battery_percent_and_temp": "100% 0°F"}

            # update data
            veh = self.vehicle.__copy__()
            ind = len(veh.velocity) - 1
            current_speed = vehicle.velocity[ind]
            throttle_force = vehicle.throttle[ind]
            brake_force = vehicle.braking_force[ind]
            steering_angle = vehicle.steering_angle[ind]
            battery_temperate = 0
            battery_percent = 100

            throttle_percent = int(10 * ((throttle_force+1) / 256))
            brake_percent = int(10 * ((brake_force+1) / 256))

            # Battery Img
            battery_img = "static/icons/battery" + str(min(math.ceil(battery_percent * 4 / 100), 4)) + ".png"

            con_png = ("static/icons/radio.png", "static/icons/radio_weak.png",
                       "static/icons/radio_active.png")[veh.radio_state]

            return {"speed": current_speed,
                    "throttle": throttle_percent,
                    "brake": brake_percent,
                    "steering_angle": steering_angle,
                    "battery_img": battery_img,
                    "con_png": con_png,
                    "battery_percent_and_temp": f"{battery_percent}% {battery_temperate}°F"}


        # Server Start
        print(f"{config.get_time()}:Webapp: Started")
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level=logging.WARNING)