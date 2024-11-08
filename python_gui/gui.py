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
        self.vehicle = vehicle

        app = FastAPI()
        self.current_speed = 0  # vehicle.velocity[0]
        self.max_speed = 100  ## from config
        self.direction = 0  # vehicle.direction[0]
        self.throttle_force = 0  # vehicle.throttle[0]
        self.max_throttle_force = 100  ## from config
        self.brake_force = 0  # vehicle.braking_force[0]
        self.max_brake_force = 50  ## from config
        self.steering_angle = 0  # vehicle.steering_angle[0]
        self.max_steering_angle = 90  ## from config
        self.battery_percent = 100
        self.battery_temp = 50

        self.responce_text = ""

        ### Resources

        app.mount("/static", StaticFiles(directory="python_gui/static"), name="static")

        ### HTML File

        @app.get("/", response_class=HTMLResponse)
        async def read_index():
            with open("python_gui/index.html", 'r') as f:
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
                return {"speed": 100,
                        "speed_meter": "static/icons/Speed9.png",
                        "throttle": 100,
                        "brake": 100,
                        "steering_notch_x": 100,
                        "steering_notch_y": 100,
                        "steering_angle": 100,
                        "battery_img": "static/icons/battery0.png",
                        "battery_percent": 100,
                        "battery_temp": 100}

            ## update data
            veh = self.vehicle.__copy__()
            ind = len(veh.velocity) - 1
            self.current_speed = vehicle.velocity[ind]
            self.max_speed = 100  ## from config
            self.direction = vehicle.direction[ind]
            self.throttle_force = vehicle.throttle[ind]
            self.max_throttle_force = 100  ## from config
            self.brake_force = vehicle.braking_force[ind]
            self.max_brake_force = 50  ## from config
            self.steering_angle = vehicle.steering_angle[ind]
            self.max_steering_angle = 90  ## from config
            self.battery_temp = vehicle.battery_temperate[ind]
            ###self.battery_percent = uh

            # Speed meter
            speed_meter = min(math.ceil(self.current_speed * 9 / self.max_speed), 9)
            speed_meter_source = "static/icons/Speed" + str(speed_meter) + ".png"

            # Throttle
            throttle_percent = 100 * self.throttle_force / self.max_throttle_force

            # Brake
            brake_percent = 100 * self.brake_force / self.max_brake_force

            # Steering Angle
            steering_notch_x = (2 * self.steering_angle / self.max_steering_angle) * math.cos(
                math.radians(self.steering_angle))
            steering_notch_y = (30 * self.steering_angle / self.max_steering_angle) * math.sin(
                math.radians(self.steering_angle))

            # Battery Img
            battery_img = "static/icons/battery" + str(min(math.ceil(self.battery_percent * 4 / 100), 4)) + ".png"

            # Send

            return {"speed": self.current_speed,
                    "speed_meter": speed_meter_source,
                    "throttle": throttle_percent,
                    "brake": brake_percent,
                    "steering_notch_x": steering_notch_x,
                    "steering_notch_y": steering_notch_y,
                    "steering_angle": self.steering_angle,
                    "battery_img": battery_img,
                    "battery_percent": self.battery_percent,
                    "battery_temp": self.battery_temp}

        ### Server Start
        print(f"{config.get_time()}:Webapp: Started")
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level=logging.WARNING)

