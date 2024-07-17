from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont
from shapely.geometry import Polygon
from datetime import datetime
import cv2
import os
import json
import matplotlib.pyplot as plt
import numpy as np
import time

def aruco_display(corners, ids, rejected, image):
	if len(corners) > 0:
		
		ids = ids.flatten()
		
		for (markerCorner, markerID) in zip(corners, ids):
			
			corners = markerCorner.reshape((4, 2))
			(topLeft, topRight, bottomRight, bottomLeft) = corners
			
			topRight = (int(topRight[0]), int(topRight[1]))
			bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
			bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
			topLeft = (int(topLeft[0]), int(topLeft[1]))

			cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
			cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
			cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
			cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)
			
			cX = int((topLeft[0] + bottomRight[0]) / 2.0)
			cY = int((topLeft[1] + bottomRight[1]) / 2.0)
			cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)
			
			cv2.putText(image, str(markerID),(topLeft[0], topLeft[1] - 10), cv2.FONT_HERSHEY_SIMPLEX,
				0.5, (0, 255, 0), 2)
			print("[Inference] ArUco marker ID: {}".format(markerID))
			
	return image

model_path = 'Train_data/segment/train4/weights/best.pt'
# video_path = 'Videos/Pez1_con_campo.mp4'
video_path = 'Videos/sample.mp4'

# Initialize YOLO model
model = YOLO(model_path)

# Open the video capture
cap = cv2.VideoCapture(video_path)

# Check if the video opened successfully
if not cap.isOpened():
    print("Error opening video file")
    exit()

# Set the start time in miliseconds (i.e. 1:35 is 95000)
start_time_ms = 0
cap.set(cv2.CAP_PROP_POS_MSEC, start_time_ms)

# Get the frame rate of the video
fps = cap.get(cv2.CAP_PROP_FPS)

# Calculate time between frames
time_difference = 1 / fps  # At constant frame rate

# Initialize a list to store dictionaries for each frame
frames_data = []

# Initialize variables for previous centroid and time
prev_centroid = None
prev_time = None

# Process each frame in the video
for frame_num in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))):
    ret, frame = cap.read()
    if not ret:
        break
    
    timer = cap.get(cv2.CAP_PROP_POS_MSEC)
    seconds = timer / 1000
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    formatted_time = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}:{int((seconds - int(seconds)) * 1000):03d}"
    # Convert frame to PIL image for YOLO processing
    img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # Get results from YOLO model
    results = model(img_pil)
    result = results[0]
    masks = result.masks

    # Initialize dictionary for current frame
    frame_data = {
        'frame_number': frame_num,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f'),
        'video_timestamp': formatted_time,
        'detected': masks is not None,
        'centroids': [],
        'velocity': [],
        'distance': 0  
    }

    # Check there are masks in the current frame to avoid errors
    if masks is not None:
        overlay = Image.new('RGBA', img_pil.size, (255, 255, 255, 0))
        overlay_draw = ImageDraw.Draw(overlay)

        for mask in masks:
            polygon = mask.xy[0]
            if len(polygon) >= 3:
                overlay_draw.polygon(polygon, outline=(0, 255, 0), fill=(0, 255, 0, 127))

                polygon_shapely = Polygon(polygon)
                centroid = polygon_shapely.centroid
                frame_data['centroids'].append((centroid.x, centroid.y))  # Append centroid coordinates to the list
                circle_radius = 5
                left_up_point = (centroid.x - circle_radius, centroid.y - circle_radius)
                right_down_point = (centroid.x + circle_radius, centroid.y + circle_radius)
                overlay_draw.ellipse([left_up_point, right_down_point], fill=(0, 0, 255))

                # Calculate velocity using time difference
                if prev_centroid is not None:
                    velocity_x = (centroid.x - prev_centroid[0]) / time_difference
                    velocity_y = (centroid.y - prev_centroid[1]) / time_difference
                    frame_data['velocity'] = [velocity_x, velocity_y]
                # Calculate distance between centroids in consecutive frames
                    distance = np.sqrt((centroid.x - prev_centroid[0])**2 + (centroid.y - prev_centroid[1])**2)
                    frame_data['distance'] = distance
            else:
                frame_data['detected'] = False

        img_pil = Image.alpha_composite(img_pil.convert("RGBA"), overlay)
        
        # Update previous centroid and time
        prev_centroid = frame_data['centroids'][-1] if frame_data['centroids'] else None
        prev_time = frame_num / fps

    # Add text overlay for frame number or timer
    draw = ImageDraw.Draw(img_pil)
    font = ImageFont.truetype("arial.ttf", 24)
    # timer = cap.get(cv2.CAP_PROP_POS_MSEC)
    # min = time.strftime('%H:%M:%S', time.gmtime(timer/1000))
    # text = f"Frame: {frame_num}"
    draw.text((10, 10), str(formatted_time), (255, 255, 255), font=font)

    frame = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    cv2.imshow("Video", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

    # Append frame data to frames_data list
    frames_data.append(frame_data)

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()

# # Print frames_data
# for frame_data in frames_data:
#     print(frame_data)

output_dir = 'Generated_data'
os.makedirs(output_dir, exist_ok=True)

file_name = 'Fish_data.json'
output_path = os.path.join(output_dir, file_name)

# Check if the file already exists
file_exists = os.path.isfile(output_path)

if file_exists:
    # If the file exists, find a unique name by adding a number at the end
    file_count = 1
    while True:
        new_file_name = f'Fish_data_{file_count}.json'
        new_output_path = os.path.join(output_dir, new_file_name)
        if not os.path.isfile(new_output_path):
            output_path = new_output_path
            break
        file_count += 1

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(frames_data, f, ensure_ascii=False, indent=4)
