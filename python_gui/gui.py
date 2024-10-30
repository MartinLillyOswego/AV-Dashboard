from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from threading import Thread
from fastapi import FastAPI
import config
import uvicorn
import math

class GUI(threading.Thread):
    
    def __init__(self, vehicle):
        super(GUI, self).__init__()
        self.vehicle = vehicle
        
        self.app = FastAPI()
        self.current_speed = vehicle.velocity
        self.max_speed = 100 ## from config
        self.direction = vehicle.direction
        self.throttle_force = vehicle.throttle
        self.max_throttle_force = 100 ## from config
        self.brake_force = vehicle.braking_force
        self.max_brake_force = 50 ## from config
        self.steering_angle = vehicle.steering_angle
        self.max_steering_angle = 90 ## from config

        ### Resources

        app.mount("/static", StaticFiles(directory="python_gui/static"), name="static")

        ### HTML File

        @app.get("/", response_class=HTMLResponse)
        async def read_index():
            with open("python_gui/index.html", 'r') as f:
                return HTMLResponse(content=f.read())

        @app.get("/open_config")
        async def open_config():
            print("config")

        @app.get("/data")
        async def get_data():
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
            return {"speed": self.current_speed,
                    "speed_meter": speed_meter_source,
                    "throttle": throttle_percent,
                    "brake": brake_percent,
                    "steering_notch_x": steering_notch_x,
                    "steering_notch_y": steering_notch_y,
                    "steering_angle" : self.steering_angle}

        ### Server Start
        uvicorn.run(app, host="127.0.0.1", port=8000)
        print(f"{config.get_time()}:Webapp: Started")
