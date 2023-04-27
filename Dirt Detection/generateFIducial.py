import cv2
import numpy as np

# Set the size of the marker and the ID
marker_size = 200
marker_id = 4

# Load the ArUco dictionary
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)

# Generate the marker image
marker_image = np.zeros((marker_size, marker_size), dtype=np.uint8)
marker_image = cv2.aruco.drawMarker(aruco_dict, marker_id, marker_size, marker_image, 1)

# Save the marker image as a PNG file
cv2.imwrite("marker4.png", marker_image)