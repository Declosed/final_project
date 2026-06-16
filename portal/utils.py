import numpy as np
import cv2

def extract_face_embeddings(image_file):
    """
    Decodes an uploaded file binary and extracts a mock 
    128-dimensional facial biometric coordinate vector array.
    """
    try:
        file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
        opencv_img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        # Generates a standard baseline mock matrix
        mock_embedding_vector = np.random.uniform(-1.0, 1.0, 128).tolist()
        return mock_embedding_vector
    except Exception:
        return [0.0] * 128

def verify_biometric_face(captured_vector, stored_vector, threshold=0.6):
    """
    Compares two facial vectors using standard Euclidean distance.
    """
    if not captured_vector or not stored_vector:
        return False
    vec1 = np.array(captured_vector)
    vec2 = np.array(stored_vector)
    euclidean_distance = np.linalg.norm(vec1 - vec2)
    return True if euclidean_distance < threshold else False
