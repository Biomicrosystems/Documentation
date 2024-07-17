import cv2 
import numpy as np 
import matplotlib.pyplot as plt
from PIL import Image
import time
from skimage.measure import label, regionprops, centroid

# Parameters
video_path = 'Videos/pez4.-sincampo.mp4'
start_time = 90  # 1 minute 30 seconds
display_width = 800
display_height = 600

mask = Image.open('mask.png')
mask = np.asarray(mask)
slice_3 = mask[:, :, 3]
new_mask = np.repeat(slice_3[:, :, np.newaxis], 3, axis=2)
new_mask = new_mask / 255.0  # Normalize new_mask to have values in the range [0, 1]


# Function to seek to a specific time in the video
def seek_to_time(cap, time_sec):
    cap.set(cv2.CAP_PROP_POS_MSEC, time_sec * 1000)

cap = cv2.VideoCapture(video_path)
seek_to_time(cap, start_time)


prev_gray = None

# Create background subtractor object
foreground_background = cv2.createBackgroundSubtractorMOG2()

def remove_small(slc, c=0.0001):
    new_slc = slc.copy()
    max_area = slc.shape[0]*slc.shape[1]
    labels = label(slc,connectivity=1,background=0)
    rps = regionprops(labels)
    areas = np.array([r.area for r in rps])
    idxs = np.where(areas/(max_area) < c)[0]
    for i in idxs:
        new_slc[tuple(rps[i].coords.T)] = 0
    return new_slc

def calculate_centroids(slc):
    labels = label(slc, connectivity=1, background=0)
    rps = regionprops(labels)
    centroids = [r.centroid for r in rps]
    return centroids

while True:
    # start time to calculate FPS
    start = time.time()

    suc, frame = cap.read()

    if not suc:
        break
    
    
    tl = (700,80); tr = (1460,100)
    bl = (670,710); br = (1440,750)

    cv2.line(frame, tl, tr, (255, 0, 0), 2)  # Draw a line between top left and top right
    cv2.line(frame, tr, br, (255, 0, 0), 2)  # Draw a line between top right and bottom right
    cv2.line(frame, br, bl, (255, 0, 0), 2)  # Draw a line between bottom right and bottom left
    cv2.line(frame, bl, tl, (255, 0, 0), 2)  # Draw a line between bottom left and top left

    s = frame.shape
    pts1 = np.float32([tl, bl, tr, br])
    pts2 = np.float32([[0,0],[0,s[0]],[s[1],0],[s[1],s[0]]])

    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(frame, matrix, (s[1], s[0]))
    
    # Multiply new_mask with result
    masked_result = result * new_mask
    new_m = masked_result.astype(np.uint8)
    
    frame = new_m
    # Apply background subtraction
    fg_mask = foreground_background.apply(new_m)
    
    # Threshold the foreground mask to get binary image
    _, binary_mask = cv2.threshold(fg_mask, 244, 255, cv2.THRESH_BINARY)
    
    small_mask = remove_small(binary_mask, c=0.00009)
    
    # Calculate centroids of the remaining blobs
    centroids = calculate_centroids(small_mask)
    
    # Draw centroids on the original frame
    for centroid in centroids:
        cv2.circle(frame, (int(centroid[1]), int(centroid[0])), 5, (0, 255, 0), -1)
    
    # Show the original video with centroids
    cv2.imshow('Original Video', cv2.resize(binary_mask, (display_width, display_height)))

    cv2.imshow('Filterd Video', cv2.resize(small_mask, (display_width, display_height)))
    
    # Break the loop when 'q' key is pressed
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()
