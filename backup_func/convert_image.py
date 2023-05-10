from PIL import Image
from pathlib import Path
import os
from pillow_heif import register_heif_opener

register_heif_opener()

# heic_file = Image.open("/Users/anhhoang.chu/Documents/google-photos-api/downloads/IMG_0653.heic")

image_dir = "./tony/"
output_dir = "./tony/processed"
Path(output_dir).mkdir(exist_ok=True)

for filename in os.listdir(image_dir):
    if filename.lower().endswith('.heic'):
        # Open the HEIC file
        heic_file = Image.open(os.path.join(image_dir, filename))

        # Convert to JPEG format
        jpeg_filename = os.path.splitext(filename)[0] + '.jpg'
        heic_file.save(os.path.join(output_dir, jpeg_filename), 'JPEG')

