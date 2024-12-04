from datetime import datetime
import json
from camera import capture_image_from_camera
import argparse
import requests

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--substation", type=str, help="Substation ID", required=True)
    args = parser.parse_args()
    substation_id = args.substation
    if substation_id:
        capture_image_from_camera(substation_id)
        json_file_path = f'{substation_id}.json'

        # Read the event data from the JSON file
        with open(json_file_path, 'r') as file:
            events_data = json.load(file)

        for event in events_data:
            event_id = event["event_id"]
            substation_id = event["SubstationId"]
            image_url = event["event_url"]
            timestamp = datetime.strptime(event["timestamp"], "%Y-%m-%dT%H:%M:%S")
            event_type = event.get("event_type", "face")  # Default to face if no type is provided

            url = "http://127.0.0.1:8000/add-event"

            # Open the image file in binary mode
            with open(image_url, "rb") as file:
                # Prepare the data and files
                data = {
                    "event_id": event_id,
                    "substation_id": substation_id,
                    "timestamp": timestamp.isoformat(),
                    "event_type": event_type,
                }
                files = {"file": file}

                # Send the POST request
                response = requests.post(url, data=data, files=files)

                # Print the response from the server
                print(response.text)
            
