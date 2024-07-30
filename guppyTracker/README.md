![alt text](https://github.com/rodhervan/guppyTracker/blob/main/static/banner.png)

This repository constains the code necessary for tracking guppy fishes and obtaining their position, distance and velocity.

## Getting started

The following steps indicate how to set up the code on a local machine.

### Prerequisites

- Python 3.11.5 or higher
- pip package manager
- git

### Installation
1. Navigate to the folder where the project files are going to be:
```bash
   cd your/path/to/project
```
2. Clone this repository:
```bash
   git clone https://github.com/rodhervan/guppyTracker
```
3. Navigate to the project directory:
```bash
   cd  guppyTracker
```
4. It is highly recommended to create a virtual environment (although optional), for this make sure venv is installed or install it from terminal
```bash
   pip install virtualenv
```
Create the virtual environment and activate it:
```bash
   python -m venv guppyEnv
   guppyEnv\Scripts\activate
```
- (OPTIONAL) If using a CUDA GPU to speed up the inference time, make sure to install the corresponding pytorch library. For example for CUDA version 11.8 execute the command:
```bash
   pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```
   You can check the different versions and options at https://pytorch.org/get-started/locally/

4. Install the other prerequisite libraries:
```bash
   pip install -r requirements.txt
```

## Usage

### Using the App

To use the app run the App.py file, then open your web browser and go to http://localhost:5000. 

This playlist shows a set of tutorials of how to run the app, annotate images and train a different model:

https://www.youtube.com/watch?v=H4wPTKL3xQY&list=PLkJ0FVEbgQ8oJraEXlRPcLOidJ2wUixhY

Google account credentials:
guppytracker24@gmail.com
Password: Biomicro2024
### Loading a video

The file yoloPredict.py loads an `.mp4` video and extracts the position of the fish using a YOLOv8 segmentation model. A pretrained model for this project is located inside the Train_data folder; traning models end in a `.pt` extension. To set the start time to something different than cero change the variable `start_time_ms` to a different value in miliseconds. This code will initiate a window showing the video an will put a green polygon to indicate the outline of the fish; a blue circle will indicate the centroid of this polygon. This window will continue to reproduce the video until it ends; to stop the video playback press the letter `Q`. Once the video playback ends and `.JSON` file will be generated containing the data extracted from the video. 

#### JSON File structure

The `.JSON` file contains a list of dictionaries, where each item in this list corresponds to a single frame. In each frame the following data will be stored under the following keys:
- `"frame_number"`: Contains an integer, where the first frame will start as 0 and increase by 1 for each frame.
- `"timestamp"`: This value corresponds to the current time when the detection was done. It saves the data in a string as `YYYY-MM-dd HH:MM:SS:fffff`.
- `"video_timestamp"`: This value is the timestamp of the video, independent from the start position, it has a structure of `HH:MM:SS:fff`.
- `"detected"`: If a fish was detected in the current frame this boolean value will be set to True, False otherwise.
- `"centroids"`: This value is a list of floats containing the x and y coordinates of the detected fish (in units pixels).
- `"velocity"`: Similar to centroids it is a list of floats that contains the x and y components of the velocity vector of a fish (it is computed on consecutive frames). 
- `"distance"`: This is a single float value, indicating the distance moved in between frames. 

### Heat map
The data generated from the `.JSON` file can be read in the heatmap.ipynb notebook. In this notebook a sample image is loaded as background (but should be replaced for different videos). The position of the fish gets used to generate a heatmap and show on top of this image the places where the fish was more frequently at during the test. 

