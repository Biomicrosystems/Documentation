import os
import json
import numpy as np
import cv2
import csv
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

def save_json(frames_data):
    output_dir = 'Generated_data'
    os.makedirs(output_dir, exist_ok=True)

    file_name = 'Fish_data.json'
    output_path = os.path.join(output_dir, file_name)

    file_exists = os.path.isfile(output_path)

    if file_exists:
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

    return output_path

def generate_graphs(json_path):
    # Load JSON data
    with open(json_path, 'r') as f:
        data = json.load(f)

    output_dir = 'Generated_data'
    graphs = []

    # Conversion factor from pixels to mm
    conversion_factor = 38 / 45

    # Plot 1: Detected Object Positions
    detected_data = [item['centroids'][0] for item in data if item.get('detected') and 'centroids' in item]
    if detected_data:
        x_positions = [centroid[0] for centroid in detected_data]
        y_positions = [centroid[1] for centroid in detected_data]

        # Convert positions from pixels to mm
        x_positions_mm = [x * conversion_factor for x in x_positions]
        y_positions_mm = [y * conversion_factor for y in y_positions]

        # Load and resize the image
        image = cv2.imread('blend_test.png')
        image_height, image_width = image.shape[:2]
        scaled_width = int(image_width * conversion_factor)
        scaled_height = int(image_height * conversion_factor)
        scaled_image = cv2.resize(image, (scaled_width, scaled_height))

        plt.imshow(cv2.cvtColor(scaled_image, cv2.COLOR_BGR2RGB))
        plt.scatter(x_positions_mm, y_positions_mm, color='red', marker='.', s=10)
        plt.xlabel('Y Position (mm)')
        plt.ylabel('X Position (mm)')
        plt.title('Detected Object Positions')
        plt.grid(True)
        plot_path = os.path.join(output_dir, 'positions_plot.png')
        plt.savefig(plot_path)
        plt.close()
        graphs.append('positions_plot.png')

    # Plot 2: Detected Object Heatmap
    if detected_data:
        heatmap, xedges, yedges = np.histogram2d(x_positions_mm, y_positions_mm, bins=30)
        plt.imshow(cv2.cvtColor(scaled_image, cv2.COLOR_BGR2RGB))
        plt.imshow(heatmap.T, extent=[xedges[0], xedges[-1], yedges[-1], yedges[0]], alpha=0.8, cmap='hot')
        plt.colorbar(label='Frequency')
        plt.xlabel('Y Position (mm)')
        plt.ylabel('X Position (mm)')
        plt.title('Detected Object Heatmap')
        plot_path = os.path.join(output_dir, 'heatmap_plot.png')
        plt.savefig(plot_path)
        plt.close()
        graphs.append('heatmap_plot.png')

    # Plot 3: Velocity Magnitude vs Time
    timestamps = []
    velocities = []
    for item in data:
        if item.get('detected') and 'velocity' in item:
            velocity = item['velocity']
            if len(velocity) == 2:
                timestamps.append(item['timestamp'])
                velocities.append(velocity)

    if timestamps and velocities:
        time_format = '%Y-%m-%d %H:%M:%S:%f'
        timestamps_dt = [datetime.strptime(timestamp, time_format) for timestamp in timestamps]
        start_time = timestamps_dt[0]
        timestamps_in_seconds = [(timestamp - start_time).total_seconds() for timestamp in timestamps_dt]
        velocities_mm = [[v[0] * conversion_factor, v[1] * conversion_factor] for v in velocities]
        vel_magnitudes_mm = [np.sqrt(velocity[0]**2 + velocity[1]**2) for velocity in velocities_mm]

        filtered_timestamps_vel = []
        filtered_velocities = []
        for i in range(len(vel_magnitudes_mm)):
            if vel_magnitudes_mm[i] <= 1200:
                filtered_timestamps_vel.append(timestamps_in_seconds[i])
                filtered_velocities.append(vel_magnitudes_mm[i])

        average_velocity = np.mean(filtered_velocities)

        plt.figure(figsize=(10, 6))
        plt.plot(filtered_timestamps_vel, filtered_velocities, marker='o', label='Velocity')
        plt.axhline(y=average_velocity, color='r', linestyle='--', label='Average Velocity')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Velocity Magnitude (mm/s)')
        plt.title('Velocity Magnitude vs Time (Filtered)')
        plt.legend()
        plt.grid(True)
        plot_path = os.path.join(output_dir, 'velocity_plot.png')
        plt.savefig(plot_path)
        plt.close()
        graphs.append('velocity_plot.png')

    # Plot 4: Distance vs Time
    timestamps = []
    distances = []
    for item in data:
        if item.get('detected') and 'distance' in item:
            timestamps.append(item['timestamp'])
            distances.append(item['distance'])

    if timestamps and distances:
        distances_mm = [distance * conversion_factor for distance in distances]
        time_format = '%Y-%m-%d %H:%M:%S:%f'
        timestamps_dt = [datetime.strptime(timestamp, time_format) for timestamp in timestamps]
        start_time = timestamps_dt[0]
        timestamps_in_seconds = [(timestamp - start_time).total_seconds() for timestamp in timestamps_dt]

        filtered_timestamps_dist = []
        filtered_distances = []
        for i in range(1, len(distances_mm)):
            if abs(distances_mm[i] - distances_mm[i-1]) <= 150:
                filtered_timestamps_dist.append(timestamps_in_seconds[i])
                filtered_distances.append(distances_mm[i])

        average_distance = np.mean(filtered_distances)

        plt.figure(figsize=(10, 6))
        plt.plot(filtered_timestamps_dist, filtered_distances, marker='o', label='Distance')
        plt.axhline(y=average_distance, color='r', linestyle='--', label='Average Distance')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Distance (mm)')
        plt.title('Distance vs Time (Filtered)')
        plt.legend()
        plt.grid(True)
        plot_path = os.path.join(output_dir, 'distance_plot.png')
        plt.savefig(plot_path)
        plt.close()
        graphs.append('distance_plot.png')

    return graphs

def generate_dataframe(json_path):
    # Load JSON data
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)

    # Generate column names based on the maximum number of detections
    max_detections = max(len(frame['centroids']) for frame in data)
    columns = ['frame_number', 'timestamp', 'video_timestamp']
    for i in range(1, max_detections + 1):
        columns.extend([f'centroid x{i}', f'centroid y{i}', f'velocity x{i}', f'velocity y{i}', f'distance{i}'])

    # Prepare data for DataFrame
    rows = []
    for frame in data:
        row = {
            'frame_number': frame['frame_number'],
            'timestamp': frame['timestamp'],
            'video_timestamp': frame['video_timestamp'],
        }

        if frame['detected']:
            for i in range(max_detections):
                if i < len(frame['centroids']):
                    centroid = frame['centroids'][i]
                    velocity = frame['velocity'] if frame['velocity'] else [None, None]
                    row.update({
                        f'centroid x{i+1}': centroid[0],
                        f'centroid y{i+1}': centroid[1],
                        f'velocity x{i+1}': velocity[0],
                        f'velocity y{i+1}': velocity[1],
                        f'distance{i+1}': frame['distance']
                    })
                else:
                    row.update({
                        f'centroid x{i+1}': None,
                        f'centroid y{i+1}': None,
                        f'velocity x{i+1}': None,
                        f'velocity y{i+1}': None,
                        f'distance{i+1}': None
                    })
        else:
            for i in range(max_detections):
                row.update({
                    f'centroid x{i+1}': None,
                    f'centroid y{i+1}': None,
                    f'velocity x{i+1}': None,
                    f'velocity y{i+1}': None,
                    f'distance{i+1}': None
                })

        rows.append(row)

    # Create DataFrame
    df = pd.DataFrame(rows, columns=columns)
    return df

def save_csv(df, base_name, output_dir='Generated_data'):
    # Write to CSV
    csv_file_path = os.path.join(output_dir, f'{base_name}.csv')
    df.to_csv(csv_file_path, index=False)
    return csv_file_path

def save_excel(df, base_name, output_dir='Generated_data'):
    # Write to Excel
    excel_file_path = os.path.join(output_dir, f'{base_name}.xlsx')
    df.to_excel(excel_file_path, index=False)
    return excel_file_path

def save_csv_and_excel(json_path):
    df = generate_dataframe(json_path)
    base_name = os.path.basename(json_path).replace('.json', '')

    csv_path = save_csv(df, base_name)
    excel_path = save_excel(df, base_name)

    return csv_path, excel_path