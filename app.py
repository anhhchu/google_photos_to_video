# Import
import pickle
import os
import shutil
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
import requests
from pathlib import Path
from PIL import Image

import pandas as pd
from datetime import date, timedelta, datetime
import json

from pathlib import Path
import face_recognition
from collections import Counter

from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from moviepy.editor import *

import cv2
import numpy as np
import argparse
DEFAULT_ENCODINGS_PATH = Path("./face_recognizer/output/encodings.pkl")

# create parser object
parser = argparse.ArgumentParser(description='Create video from images')

# add arguments to the parser object
parser.add_argument('--date_str', type=str, help='The date to download images')
parser.add_argument('--person', type=str, help='The target person to create video')

# parse arguments
args = parser.parse_args()

# access the arguments' values
date_str = args.date_str
person = args.person

print(date_str, person)

def _recognize_face(unknown_encoding, loaded_encodings):
    """
    private function to identifying each face in the given image
    """
    boolean_matches = face_recognition.compare_faces(
        loaded_encodings["encodings"], unknown_encoding
    )
    votes = Counter(name for match, name in zip(boolean_matches, loaded_encodings["names"]) if match)
    if votes:
        return votes.most_common(1)[0][0]


def recognize_faces(
    image_location: str,
    target_face = "anh",
    model: str = "hog"
) -> None:
    """
    recognizes faces in images that don’t have a label

    Returns:
        boolean: True if match with target face, False otherwise
    """

    # load unlabeled images from validation folder
    input_image = face_recognition.load_image_file(image_location)

    # find the location for input images
    input_face_locations = face_recognition.face_locations(
        input_image, model=model
    )
    
    # extract encoding for the input images
    input_face_encodings = face_recognition.face_encodings(
        input_image, input_face_locations
    )

    target_list = []
    # use parallel iteration to match the face to encoding
    for bounding_box, unknown_encoding in zip(input_face_locations, input_face_encodings):
        name = _recognize_face(unknown_encoding, loaded_encodings)
        if not name:
            name = "Unknown"
        print(image_location, name, bounding_box)
        if name == target_face:
            return True
        return False

def create_video(image_dir, audio_file, output_dir):
    """
    Create video with images from image_dir, audio from audio_file and save to output_dir
    """

    # Get a list of all files in the download_dir
    image_files = [ os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.lower().endswith('.heic') or f.lower().endswith('.jpg') ]

    # Sort the images in ascending order based on filename
    image_files.sort()

    # Create a clip from the image sequence
    clip = ImageSequenceClip(image_files, fps=1)

    #  # Write the clip to a video file
    # clip.write_videofile(f"{date_str}.mp4", codec="libx264")

    # Load the audio file
    audioclip = AudioFileClip(audio_file)

    # Set audio duration to match the video duration
    audioclip = audioclip.set_duration(clip.duration)

    # Combine the audio and video clips
    final_clip = clip.set_audio(audioclip)

    # Write the clip to a video file
    final_clip.write_videofile(f"{output_dir}", codec="libx264", audio_codec="aac")

def pad_image(download_dir, image, target_dir):
    # extract image name
    img = cv2.imread(os.path.join(download_dir, image))
    height, width, _ = img.shape

    # Calculate the desired width and height for a 16:9 aspect ratio
    desired_width = int(height * 16 / 9)
    desired_height = height

    # Calculate the amount of padding needed
    pad_width = (desired_width - width) // 2

    # Create a black border for the padding
    border = cv2.copyMakeBorder(img, 0, 0, pad_width, pad_width, cv2.BORDER_CONSTANT, value=[0, 0, 0])

    # Resize the image to the desired size, keeping the aspect ratio
    resized = cv2.resize(border, (1920, 1080))

    # Save the resized image to disk
    cv2.imwrite(os.path.join(target_dir, image), resized)
    
if __name__ == "__main__":

    ######
    ## 1. Download Images from Google Photos for one specific day
    ######
    download_dir = f'./downloads/{date_str}'
    return_value = os.system(f"./.venv/bin/python ./download_image.py --date_str {date_str}")
    if return_value != 0:
        raise Exception(f"Error downloading images: {return_value}")

    ######
    ## 2. Detect images with only the target person face
    ######

    target_dir = f'./downloads/target/{date_str}'
    encodings_location = DEFAULT_ENCODINGS_PATH
    ## create parents dir recursively
    Path(target_dir).mkdir(parents=True, exist_ok=True)
    
    ## load saved face encoding using pickl
    print(f"---Loading encodings from {encodings_location}---")
    with encodings_location.open(mode="rb") as f:
        loaded_encodings = pickle.load(f)

    for image in os.listdir(download_dir):
        # print(filepath)
        if recognize_faces(os.path.join(download_dir, image), person):
            # shutil.copy(filepath, target_dir)
            pad_image(download_dir, image, target_dir)

    ######
    ## 3. Create video of the target person images
    ######
    # https://www.tutorialexample.com/python-moviepy-convert-different-size-images-png-jpg-to-video-python-moviepy-tutorial/
    create_video(target_dir, "./audio/vacation-beat.mp3", f"./output_videos/{date_str}.mp4")

    ######
    ## 4. Upload video back to Google Photos 
    ######

