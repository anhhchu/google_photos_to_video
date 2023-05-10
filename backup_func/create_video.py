import os
from pathlib import Path
from PIL import Image
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from moviepy.editor import *

# Define the directory containing the PNG images
date = "2022-06-11"
image_directory = f"./downloads/target/{date}"

# Get a list of all PNG files in the directory
image_files = [ os.path.join(image_directory, f) for f in os.listdir(image_directory) if f.lower().endswith('.jpg')]

# Sort the images in ascending order based on filename
image_files.sort()

# Create a clip from the image sequence
clip = ImageSequenceClip(image_files, fps=1)

#  # Write the clip to a video file
# clip.write_videofile(f"{date}.mp4", codec="libx264")

# Load the audio file
audio_file = './audio/vacation-beat.mp3'
audioclip = AudioFileClip(audio_file)

# Set audio duration to match the video duration
audioclip = audioclip.set_duration(clip.duration)

# Combine the audio and video clips
final_clip = clip.set_audio(audioclip)

# Write the clip to a video file
final_clip.write_videofile(f"{date}.mp4", codec="libx264", audio_codec="aac")



