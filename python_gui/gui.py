from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
import threading
import config
import uvicorn
import math

class GUI(threading.Thread):
    
    def __init__(self, vehicle):
        super(GUI, self).__init__()
        self.vehicle = vehicle
        
        
        app = FastAPI()
        self.current_speed = 100
        self.max_speed = 100 ## from config
        self.direction = 100
        self.throttle_force = 100
        self.max_throttle_force = 100 ## from config
        self.brake_force = 100
        self.max_brake_force = 100 ## from config
        self.steering_angle = 100
        self.max_steering_angle = 90 ## from config

        self.responce_text = ""

        ### Resources

        app.mount("/static", StaticFiles(directory="python_gui/static"), name="static")

        ### HTML File

        @app.get("/", response_class=HTMLResponse)
        async def read_index():
            with open("python_gui/index.html", 'r') as f:
                return HTMLResponse(content=f.read())

        @app.get("/open_config", response_class=HTMLResponse)
        async def open_config(serial_port: str = "", max_speed: str = ""):

            # update serial port
            if serial_port != "":
                print(f"{config.get_time()}: Updating value for serial_port")
                config.CARLA_SERIAL_PORT = serial_port
                config.VEHICLE_PORT = serial_port
                self.responce_text = "Updated Serial Port, you may need to restart the dashboard"

            # updated allowed max speed
            if max_speed != "":
                try:
                    config.MAX_SPEED = float(max_speed)
                    self.responce_text = "Updated Allowed Max Speed"
                except ValueError:
                    self.responce_text = "Invalid input for this filed"

            with open("python_gui/tuning_menu.html", 'r') as f:
                return HTMLResponse(content=f.read())

        @app.get("/config_data")
        async def get_config_data():
            out = {
                "serial_port": config.VEHICLE_PORT,
                "max_speed": config.MAX_SPEED,
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
                    "steering_angle" : 100}
            
            ## update data
            self.current_speed = vehicle.velocity[0]
            self.max_speed = 100 ## from config
            self.direction = vehicle.direction[0]
            self.throttle_force = vehicle.throttle[0]
            self.max_throttle_force = 100 ## from config
            self.brake_force = vehicle.braking_force[0]
            self.max_brake_force = 50 ## from config
            self.steering_angle = vehicle.steering_angle[0]
            self.max_steering_angle = 90 ## from config
            
            # Speed meter
            speed_meter = min(math.ceil(self.current_speed*9/self.max_speed),9)
            speed_meter_source = "static/icons/Speed" + str(speed_meter) + ".png"
            
            # Throttle
            throttle_percent = 100 * self.throttle_force / self.max_throttle_force
            
            # Brake
            brake_percent = 100 * self.brake_force / self.max_brake_force
            
            # Steering Angle
            steering_notch_x = (2*self.steering_angle/self.max_steering_angle)* math.cos(math.radians(self.steering_angle))
            steering_notch_y = (30*self.steering_angle/self.max_steering_angle)* math.sin(math.radians(self.steering_angle))
            
            # Send
           veh = self.vehicle.__copy__()
            v = 0
            ind = len(veh.velocity)-1
            if ind >= 0:
                v = veh.velocity[ind]
            return {"speed": v,
                    "speed_meter": speed_meter_source,
                    "throttle": throttle_percent,
                    "brake": brake_percent,
                    "steering_notch_x": steering_notch_x,
                    "steering_notch_y": steering_notch_y,
                    "steering_angle" : self.steering_angle}

        ### Server Start
        uvicorn.run(app, host="127.0.0.1", port=8000)
        print(f"{config.get_time()}:Webapp: Started")
