from datetime import datetime
import json
import os
from database import clear_database, create_table, store_event
from event_processing import check_event
from fastapi import FastAPI, File, UploadFile, Form
from pydantic import UUID4

app=FastAPI()
save_directory = "./central"

@app.get("/")
def index():
    return "Welcome to central server"

@app.get("/setup")
def setup():
    clear_database()
    create_table()
    os.makedirs(save_directory, exist_ok=True)  # Create the directory if it doesn't exist    

@app.post("/add-event")
async def create_upload_file(
    event_id: str = Form(...), 
    substation_id: str = Form(...), 
    timestamp: datetime = Form(...),
    event_type: str = Form(...),
    file: UploadFile = File(...)
):
    save_path = os.path.join(save_directory, f"{event_id}.png")

    with open(save_path, "wb") as f:
        content = await file.read()  # Read the uploaded file's content
        f.write(content)  # Write the content to the specified path

    # Check for duplicates or threats based on event type (face or license plate)
    event_status = check_event("server", save_path, event_type)
    store_event(event_id, substation_id, save_path, timestamp, event_type)
    print(f"{event_type.capitalize()} event {event_id} stored successfully at {timestamp} and it's a {event_status}")
    
    if "Threat" in event_status:
        print(f"Threat alert!")

    return {"message": f"{event_id} saved at central server"}
