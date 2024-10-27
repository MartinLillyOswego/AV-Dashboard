from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import math

app = FastAPI()

current_speed = 1
max_speed = 100
direction = "f"
throttle_percent = 20
brake_percent = 70

### Resources

app.mount("/static", StaticFiles(directory="static"), name="static")

### HTML File 

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", 'r') as f:
        return HTMLResponse(content=f.read())

@app.get("/speed")
async def get_speed():
    global direction
    global current_speed
    global max_speed
    global speed_meter
    global throttle_percent
    global brake_percent

    ### Speed
    if direction == "f":
        current_speed = current_speed + 1
        if current_speed == 120: direction = "b"
    else:
        current_speed = current_speed - 1
        if current_speed == 1: direction = "f"

    ### Speed meter
    speed_meter = min(math.ceil(current_speed*9/max_speed),9)
    speed_meter_source = "static/icons/Speed" + str(speed_meter) + ".png"
    
    ### Send
    return {"speed": current_speed,
            "speed_meter": speed_meter_source,
            "throttle": throttle_percent,
            "break": brake_percent}

### Server Start

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)