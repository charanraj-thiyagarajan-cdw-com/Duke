import cv2
import os
import json
import uuid
import pytesseract  # For license plate detection
from datetime import datetime

# Load Haar Cascade for face detection (you can download this file from OpenCV GitHub)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def capture_image_from_camera(substation_id):
    """Capture an image from the camera and save it to the folder."""
    os.makedirs(substation_id, exist_ok=True)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    image_captured = False  # Track whether an image has been captured

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        cv2.imshow('Camera Feed', frame)

        # Press 's' to save the image
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            event_id = str(uuid.uuid4())
            timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            image_name = f"{event_id}.png"
            save_path = os.path.join(substation_id, image_name)

            cv2.imwrite(save_path, frame)
            print(f"Image saved to {save_path}")

            # Detect if the image contains a face or a license plate
            event_type = detect_event_type(frame)

            # Add the image event to the JSON data to respective substation
            add_image_event_to_json(event_id, timestamp, save_path, event_type, substation_id)
            image_captured = True  # Mark that an image was captured

            # Exit the loop after saving the image
            break

        # Press 'q' to quit
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Check if an image was captured
    if not image_captured:
        print("Failed to capture image. Exiting.")
    else:
        print("Image capture completed successfully.")

def detect_event_type(frame):
    """Detect whether the image contains a face or a license plate."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Check for license plates in the image using Tesseract
    text = pytesseract.image_to_string(frame)
    if is_license_plate(text):
        return "license_plate"
    # Check for faces in the image
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if len(faces) > 0:
        return "face"

    

    # If no face or license plate is detected
    return "unknown"

def is_license_plate(text):
    """Simple heuristic to check if the detected text is a license plate."""
    if len(text) >= 0 and any(char.isdigit() for char in text):
        return True
    return False

def add_image_event_to_json(event_id, timestamp, image_path, event_type, substation_id):
    """Add a new image event to the JSON data in events_data.json."""
    new_event = {
        "event_id": event_id,
        "timestamp": timestamp,
        "event_url": image_path,
        "SubstationId": substation_id,
        "event_type": event_type
    }

    # Check if the JSON file exists; if not, create an empty list
    if not os.path.exists(f'{substation_id}.json'):
        events_data = []
    else:
        # Load existing data from respective substation
        with open(f'{substation_id}.json', 'r') as file:
            events_data = json.load(file)

    # Append the new event to the data
    events_data.append(new_event)

    # Write the updated data back to respective substation
    with open(f'{substation_id}.json', 'w') as file:
        json.dump(events_data, file, indent=4)

    print(f"Event {event_id} added with timestamp {timestamp} and event type {event_type}.")

