import cv2
import os
from os.path import join, dirname, exists

# Define the directory to save photos
photos_dir = join(dirname(__file__), "photos")

# Ensure the directory exists
if not exists(photos_dir):
    os.makedirs(photos_dir)

# Define the path for the text file to store the current photo ID
photo_id_file = join(photos_dir, "photo_id.txt")

def get_next_photo_id():
    if not exists(photo_id_file):
        return 1
    with open(photo_id_file, "r") as f:
        last_id = int(f.read().strip())
        return last_id + 1

def save_photo_id(photo_id):
    with open(photo_id_file, "w") as f:
        f.write(f"{photo_id}")

def capture_photo():
    # Open the first camera connected to the system
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return None

    # Capture a single frame
    ret, frame = cap.read()

    # Release the camera
    cap.release()

    if ret:
        return frame
    else:
        print("Error: Could not capture photo.")
        return None

def save_photo(frame):
    photo_id = get_next_photo_id()
    photo_path = join(photos_dir, f"photo{photo_id}.png")
    cv2.imwrite(photo_path, frame)
    save_photo_id(photo_id)
    print(f"Photo saved as {photo_path}")
    return photo_path, photo_id


def permanent_photo_delete(photo_id):
    # Construct the path to the photo
    photo_path = join(photos_dir, f"photo{photo_id}.png")
    
    # Print the full path to ensure it's correct
    print(f"Looking for file: {os.path.abspath(photo_path)}")
    
    # Check if the directory exists
    if not os.path.exists(os.path.dirname(photo_path)):
        print(f"Directory 'photos' does not exist.")
        return
    
    # Check if the file exists
    if not os.path.isfile(photo_path):
        print(f"Photo {photo_id} does not exist at {photo_path}.")
        return
    
    # Delete the photo permanently
    os.remove(photo_path)
    print(f"Photo {photo_id} has been deleted permanently.")


