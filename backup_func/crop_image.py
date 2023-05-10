# from PIL import Image

# # Set the dimensions of the desired crop
# crop_width, crop_height = 1920, 1080

# # Open the image file
# image = Image.open("face_recognizer/training/anh/4E38373E-BD31-425D-9645-CE7BA59FC381.jpg")

# # Get the dimensions of the image
# image_width, image_height = image.size

# # Calculate left, upper, right, and lower pixel coordinates of the crop area
# left = (image_width - crop_width) / 2
# upper = (image_height - crop_height) / 2
# right = (image_width + crop_width) / 2
# lower = (image_height + crop_height) / 2

# # Crop the image using the calculated pixel coordinates
# cropped_image = image.crop((left, upper, right, lower))

# # Save the cropped image to a new file
# cropped_image.save("downloads/crop")
import os
from PIL import Image, ImageOps
 
image_dir = "./downloads/target/2022-06-11"
crop_dir = "./video-from-image/downloads/crop"

# Get a list of all image files in the directory
image_files = [  f for f in os.listdir(image_dir) if f.lower().endswith('.jpg')]

 
width, height = 1440, 1800


for image in image_files:
    img = Image.open(f"{image_dir}/{image}")
    # compute the crop box to preserve the center of the image
    center_x, center_y = img.width / 2, img.height / 2
    half_width, half_height = width / 2, height / 2
    left, top, right, bottom = center_x - half_width, center_y - half_height, center_x + half_width, center_y + half_height
    crop_box = (int(left), int(top), int(right), int(bottom))

    # crop the image to the desired dimensions
    img = img.crop(crop_box)

    # save the cropped image
    img.save(f"{crop_dir}/{image}")
