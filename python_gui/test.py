from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

# Serve static files (e.g., CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

current_speed = 1
direction = "f"

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", 'r') as f:
        return HTMLResponse(content=f.read())

@app.get("/speed")
async def get_speed():
    global direction
    global current_speed
    if direction == "f":
        current_speed = current_speed + 1
        if current_speed == 120: direction = "b"
    else:
        current_speed = current_speed - 1
        if current_speed == 1: direction = "f"
    return {"speed": current_speed}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)