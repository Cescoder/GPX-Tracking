from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Tuple
from pydantic import BaseModel
import gpxpy.gpx
from fastapi.responses import FileResponse
app = FastAPI()

class Coordinates(BaseModel):
    latitude: float
    longitude: float

class PositionList(BaseModel):
    positions: List[Coordinates]

# Configure CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to the appropriate origins or use ["http://localhost"] for development
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Add OPTIONS to the allowed methods
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_positions(obj: dict = Body(...)):#position_list: PositionList):
    print(obj)
    positions = obj["positions"]
    #now make gpx file with these coordinates
    
    gpx = gpxpy.gpx.GPX()
    for position in positions:
        gpx.waypoints.append(gpxpy.gpx.GPXWaypoint(position[0], position[1]))
    print(gpx.to_xml())

    with open("output.gpx", "w") as f:
        f.write(gpx.to_xml())
    
    #TODO: return the file
    
    return {"message": "OK"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



