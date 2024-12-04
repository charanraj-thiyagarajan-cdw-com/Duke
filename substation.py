from datetime import datetime
import time
import os
import argparse
import uuid
import requests
from camera import detect_event_type
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ImageHandler(FileSystemEventHandler):
    def __init__(self, folder_to_monitor, substation):
        self.folder_to_monitor = folder_to_monitor
        self.substion = substation

    def on_created(self, event):
        # Check if the created file is an image
        if not event.is_directory and event.src_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"New image detected: {event.src_path}")
            self.send_image(event.src_path)

    def send_image(self, file_path):
        try:
            url = "http://127.0.0.1:8000/add-event"
            
            # Open the image file in binary mode
            with open(file_path, "rb") as file:
                # Prepare the data and files
                data = {
                    "event_id": str(uuid.uuid4()),
                    "substation_id": substation_id,
                    "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                    "event_type": detect_event_type(file_path),
                }
                files = {"file": file}

                # Send the POST request
                response = requests.post(url, data=data, files=files)

                # Print the response from the server
                if response.status_code == 200:
                    print(f"Successfully sent image: {file_path}")
                else:
                    print(f"Failed to send image: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"Error sending image: {e}")

def monitor_folder(folder_to_monitor, substation):
    event_handler = ImageHandler(folder_to_monitor, substation)
    observer = Observer()
    observer.schedule(event_handler, folder_to_monitor, recursive=False)
    observer.start()
    print(f"Monitoring folder: {folder_to_monitor}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--substation", type=str, help="Substation ID", required=True)
    args = parser.parse_args()
    substation_id = args.substation
    os.makedirs(substation_id, exist_ok=True)
    if substation_id:
        folder_to_monitor = f"./{substation_id}"
        monitor_folder(folder_to_monitor, substation_id)
