from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

# Serve static files (e.g., CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

current_speed = 1
direction = "f"
throttle_percent = 60
break_percent = 100

<<<<<<< Updated upstream
=======
### Resources

app.mount("/static", StaticFiles(directory="static"), name="static")

### HTML File 

>>>>>>> Stashed changes
@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", 'r') as f:
        return HTMLResponse(content=f.read())

@app.get("/speed")
async def get_speed():
    global direction
    global current_speed
<<<<<<< Updated upstream
=======
    global speed_meter
    global throttle_percent
    global break_percent

    ### Speed
>>>>>>> Stashed changes
    if direction == "f":
        current_speed = current_speed + 1
        if current_speed == 120: direction = "b"
    else:
        current_speed = current_speed - 1
        if current_speed == 1: direction = "f"
<<<<<<< Updated upstream
    return {"speed": current_speed}
=======

    ### Speed meter
    speed_meter = min(math.ceil(current_speed*9/max_speed),9)
    speed_meter_source = "static/icons/Speed" + str(speed_meter) + ".png"
    return {"speed": current_speed,
            "speed_meter": speed_meter_source,
            "throttle": throttle_percent,
            "break": break_percent}

### Server Start
>>>>>>> Stashed changes

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)