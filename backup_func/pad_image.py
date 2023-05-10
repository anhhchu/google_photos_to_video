import cv2
import os
import numpy as np

image_dir = "./downloads/2022-06-11"
resize_dir = "./downloads/target/2022-06-11"

# Get a list of all image files in the directory
image_files = [  f for f in os.listdir(image_dir) if f.lower().endswith('.jpg')]

 
width, height = 1440, 1800


for image in image_files:
    # Get the dimensions of the image
    img = cv2.imread(f"{image_dir}/{image}")
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
    cv2.imwrite(os.path.join(resize_dir, image), resized)

