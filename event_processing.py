from datetime import datetime
from database import find_common_events
from PIL import Image
import imagehash

def compute_image_hash(image_path):
    """Compute the perceptual hash of an image for comparison."""
    with Image.open(image_path) as img:
        img = img.convert("RGB")  # Convert image to RGB for consistency
        img_hash = imagehash.phash(img)  # Compute perceptual hash
        return img_hash  # Return as an imagehash object for comparison

def compare_image_hashes(hash1, hash2, threshold=0.5):
    """Compare two image hashes and return similarity percentage."""
    difference = hash1 - hash2  # Calculate the number of differing bits
    max_difference = len(hash1.hash) * hash1.hash.shape[0]  # Total bits in hash
    similarity = 1 - (difference / max_difference)  # Calculate the similarity percentage
    return similarity

def check_event(substation_id, snapshot_path, event_type):
    # Retrieve existing events from the database
    existing_events = find_common_events(substation_id, event_type)  # This should return all events for comparison
    # Compute the hash for the new image
    new_image_hash = compute_image_hash(snapshot_path)

    for existing_event in existing_events:
        existing_time = datetime.strptime(existing_event['timestamp'], "%Y%m%d_%H%M%S")  # Updated format
        existing_substation = existing_event.get('substation')
        existing_image_path = existing_event.get('snapshot_path')
        existing_event_type = existing_event.get('event_type')  # Assuming event_type is a key in the dict
        # Filter by the event type (either face or license plate)
        if existing_event_type != event_type:
            return  # Skip this event if the type doesn't match
        
        # Compute the hash for the existing image
        existing_image_hash = compute_image_hash(existing_image_path)

        # Compare hashes to get similarity
        similarity = compare_image_hashes(new_image_hash, existing_image_hash)
        # Check if it's a duplicate (similar image hash in the same substation)
        if similarity >= 0.5 and substation_id == existing_substation:
            return f"Duplicate {event_type}"  # Similar image and same substation indicates a duplicate
    
        # Check if it's a threat (similar image hash but from different substations)
        if similarity >= 0.5 and substation_id != existing_substation:
            return f"Threat {event_type}"  # Similar image from a different substation indicates a threat
    return f"No type found for {event_type}"  # Neither a duplicate nor a threat
