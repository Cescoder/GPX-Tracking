#LIBRARIES
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import gpxpy.gpx
import os
import uuid
import hashlib
import datetime

#CONSTS
HOST = '127.0.0.1'
PORT = 8000

#APP OBJECT
app = FastAPI(title='GPX API')

#MIDDLEWARE SETTINGS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#ROUTES
@app.post("/upload")
async def upload_positions(obj: dict = Body(...)):
    #getting data
    positions = obj["positions"]
    
    #writing gpx xml
    gpx = gpxpy.gpx.GPX()

    for position in positions:
        waypoint = gpxpy.gpx.GPXWaypoint(latitude=position["latitude"],longitude= position['longitude'])
        gpx.waypoints.append(waypoint)
    
    gpx_xml = gpx.to_xml()

    # Generate unique filename
    unique_id = uuid.uuid4().hex
    hash_object = hashlib.sha256(unique_id.encode())
    unique_filename = f"{hash_object.hexdigest()}.gpx"
    file_path = f'generated_files/{unique_filename}'

    # Writing file in the folder
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write(gpx_xml)
    
    # Message Responde
    return {"message": "OK", "filename": unique_filename}

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = f'generated_files/{filename}'
    
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        return {"error": "File not found"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
