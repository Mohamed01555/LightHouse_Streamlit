from deepface import DeepFace as dpf
import numpy as np
import json
import os
from numpy.linalg import norm
from PIL import ImageOps, Image

def cosine_similarity(vec1, vec2):
    """
    Calculate the cosine similarity between two vectors.
    
    Args:
    vec1 (numpy.ndarray): First vector.
    vec2 (numpy.ndarray): Second vector.

    Returns:
    float: Cosine similarity between vec1 and vec2.
    """
    return np.dot(vec1, vec2) / (norm(vec1) * norm(vec2))

# Function to encode face
def encode_face(image_path):
    #embeddings
    face_encodings = dpf.represent(
        img_path = image_path, 
        model_name = 'Facenet',
        detector_backend = 'ssd'
    )
    if face_encodings:
        return face_encodings[0]
    else:
        return None

# Save data to JSON file
def save_data(file_path, new_data):
    """ Append new data to an existing JSON file. """
    existing_data = []

    # Load existing data if file exists
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            existing_data = json.load(f)

    # Append new data to existing data
    existing_data.append(new_data)

    # Write the combined data back to the file
    with open(file_path, "w") as f:
        json.dump(existing_data, f)

# Load data from JSON file
def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    else:
        return {}

# Initialize databases
volunteer_db = "volunteer_db.json"
parent_db = "parent_db.json"

# Ensure directories for storing images exist
volunteer_images_dir = "uploaded_images/volunteers"
parent_images_dir = "uploaded_images/parents"