import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import torch
from shapely.geometry import Polygon
from ultralytics import YOLO
import base64

model_path = 'Train_data/segment/train4/weights/best.pt'
model = YOLO(model_path)

frames_data = []
prev_centroid = None
prev_time = None
cap = None
stop_processing = False

def start_video_processing(video_path, socketio, emit):
    global cap, stop_processing, frames_data, prev_centroid, prev_time

    cap = cv2.VideoCapture(video_path)
    frames_data = []
    prev_centroid = None
    prev_time = None
    stop_processing = False

    if not cap.isOpened():
        emit('error', {'message': 'Error opening video file'})
        return

    fps = cap.get(cv2.CAP_PROP_FPS)

    while cap.isOpened() and not stop_processing:
        ret, frame = cap.read()
        if not ret:
            break

        timer = cap.get(cv2.CAP_PROP_POS_MSEC)
        seconds = timer / 1000
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        formatted_time = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}:{int((seconds - int(seconds)) * 1000):03d}"

        img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Run inference with error handling and retries
        success = False
        retries = 0
        max_retries = 5
        while not success and retries < max_retries:
            try:
                results = model(img_pil)
                success = True
            except torch.backends.cudnn.CuDNNError as e:
                print(f"cuDNN error occurred: {e}")
                retries += 1
                time.sleep(1)  # Wait for a second before retrying

        if not success:
            emit('error', {'message': 'Something went wrong launching CUDA after multiple attempts'})
            break

        result = results[0]
        masks = result.masks

        frame_data = {
            'frame_number': int(cap.get(cv2.CAP_PROP_POS_FRAMES)),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f'),
            'video_timestamp': formatted_time,
            'detected': masks is not None,
            'centroids': [],
            'velocity': [],
            'distance': 0  
        }

        if masks is not None:
            overlay = Image.new('RGBA', img_pil.size, (255, 255, 255, 0))
            overlay_draw = ImageDraw.Draw(overlay)

            for mask in masks:
                polygon = mask.xy[0]
                if len(polygon) >= 3:
                    overlay_draw.polygon(polygon, outline=(0, 255, 0), fill=(0, 255, 0, 127))

                    polygon_shapely = Polygon(polygon)
                    centroid = polygon_shapely.centroid
                    frame_data['centroids'].append((centroid.x, centroid.y))
                    circle_radius = 5
                    left_up_point = (centroid.x - circle_radius, centroid.y - circle_radius)
                    right_down_point = (centroid.x + circle_radius, centroid.y + circle_radius)
                    overlay_draw.ellipse([left_up_point, right_down_point], fill=(0, 0, 255))

                    if prev_centroid is not None:
                        velocity_x = (centroid.x - prev_centroid[0]) / (1 / fps)
                        velocity_y = (centroid.y - prev_centroid[1]) / (1 / fps)
                        frame_data['velocity'] = [velocity_x, velocity_y]
                        distance = np.sqrt((centroid.x - prev_centroid[0])**2 + (centroid.y - prev_centroid[1])**2)
                        frame_data['distance'] = distance
                else:
                    frame_data['detected'] = False

            img_pil = Image.alpha_composite(img_pil.convert("RGBA"), overlay)
            prev_centroid = frame_data['centroids'][-1] if frame_data['centroids'] else None
            prev_time = cap.get(cv2.CAP_PROP_POS_FRAMES) / fps

        draw = ImageDraw.Draw(img_pil)
        font = ImageFont.truetype("arial.ttf", 24)
        draw.text((10, 10), str(formatted_time), (255, 255, 255), font=font)

        frame = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

        # Convert frame to base64 to send to client
        _, buffer = cv2.imencode('.jpg', frame)
        frame_base64 = base64.b64encode(buffer).decode('utf-8')

        emit('frame', {'frame': frame_base64, 'frame_data': frame_data})

        frames_data.append(frame_data)
        socketio.sleep(1 / fps)

    cap.release()

def stop_video_processing():
    global stop_processing
    stop_processing = True
    return frames_data
