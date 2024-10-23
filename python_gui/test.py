from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import random

app = FastAPI()
current_speed = 1
direction = "f"

app.mount("/icons", StaticFiles(directory="icons"), name="icons")


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
        if current_speed == 100: direction = "b"
    else:
        current_speed = current_speed - 1
        if current_speed == 1: direction = "f"
    return {"speed": current_speed}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)