from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import random
import math

app = FastAPI()
current_speed = 1
max_speed = 100
speed_meter = 0
direction = "f"

### Resources

app.mount("/icons", StaticFiles(directory="icons"), name="icons")

@app.get("/style.css")
async def get_css():
    return FileResponse("style.css")

### HTML File 

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", 'r') as f:
        return HTMLResponse(content=f.read())

### Data Packing

@app.get("/data")
async def get_data():
    global direction
    global current_speed
    global speed_meter

    ### Speed
    if direction == "f":
        current_speed = current_speed + 1
        if current_speed == 100: direction = "b"
    else:
        current_speed = current_speed - 1
        if current_speed == 1: direction = "f"

    ### Speed meter
    speed_meter = min(math.ceil(current_speed*9/max_speed),9)
    speed_meter_source = "icons/Speed" + str(speed_meter) + ".png"
    return {"speed": current_speed,
            "speed_meter": speed_meter_source}

### Server Start

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)