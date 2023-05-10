import face_recognition
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()

known_image_loc = "./downloads/2023-03-14/IMG_9624.HEIC"
unknown_image_loc = "./downloads/2023-03-14/IMG_9691.HEIC"

# Load the HEIC image using Pillow
image1 = Image.open(known_image_loc)
# Convert the image to RGB format
image1 = image1.convert('RGB')
print(image1)

# # Load the HEIC image using Pillow
# image2 = Image.open(unknown_image_loc)
# # Convert the image to RGB format
# image2 = image1.convert('RGB')

image_array = face_recognition.load_image_file(image1)
# print(image_array)
face_landmarks = face_recognition.face_landmarks(image_array)
my_face_encoding = face_recognition.face_encodings(image_array, face_landmarks)
print(len(my_face_encoding))

# # my_face_encoding now contains a universal 'encoding' of my facial features that can be compared to any other picture of a face!

# unknown_picture = face_recognition.load_image_file(image2)
# unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

# # Now we can see the two face encodings are of the same person with `compare_faces`!

# results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding)

# if results[0] == True:
#     print("It's a picture of me!")
# else:
#     print("It's not a picture of me!")