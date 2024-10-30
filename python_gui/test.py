from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from threading import Thread
from fastapi import FastAPI
import config
import uvicorn
import math

app = FastAPI()

current_speed = 1
max_speed = 100
direction = "f"
throttle_percent = 100
brake_percent = 100
steering_angle = 0
steering_angle_limit = max_speed ## change

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

@app.get("/speed")
async def get_speed():
    global direction
    global current_speed
    global max_speed
    global speed_meter
    global throttle_percent
    global brake_percent
    global steering_angle
    global steering_angle_limit

    # Speed
    if direction == "f":
        current_speed = current_speed + 1
        if current_speed == 100: direction = "b"
    else:
        current_speed = current_speed - 1
        if current_speed == 1: direction = "f"

    # Speed meter
    speed_meter = min(math.ceil(current_speed*9/max_speed),9)
    speed_meter_source = "static/icons/Speed" + str(speed_meter) + ".png"
    
    # Throttle
    throttle_percent = current_speed
    
    # Brake
    brake_percent = max_speed - current_speed
    
    # Steering Angle
    steering_angle = current_speed - 50  # change
    steering_notch_x = (2*steering_angle/steering_angle_limit)* math.cos(math.radians(steering_angle))
    steering_notch_y = (30*steering_angle/steering_angle_limit)* math.sin(math.radians(steering_angle))
    
    # Send
    return {"speed": current_speed,
            "speed_meter": speed_meter_source,
            "throttle": throttle_percent,
            "brake": brake_percent,
            "steering_notch_x": steering_notch_x,
            "steering_notch_y": steering_notch_y,
            "steering_angle" : steering_angle}

### Server Start
def main():
    uvicorn.run(app, host="127.0.0.1", port=8000)
thread = Thread(target=main)
thread.start()
print(f"{config.get_time()}:Webapp: Started")