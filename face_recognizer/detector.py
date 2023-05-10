from pathlib import Path
import face_recognition
import pickle
from collections import Counter

DEFAULT_ENCODINGS_PATH = Path("face_recognizer/output/encodings.pkl")

Path("face_recognizer/training").mkdir(exist_ok=True)
Path("face_recognizer/output").mkdir(exist_ok=True)
Path("face_recognizer/validation").mkdir(exist_ok=True)


def encode_known_faces(model: str = "hog", encodings_location: Path = DEFAULT_ENCODINGS_PATH) -> None:
    """
    go through each directory within training/, 
    saves the label from each directory into name, 
    use the load_image_file() function from face_recognition to load each image
    create a dictionary that puts the names and encodings lists together and denotes which list is which.  use pickle to save the encodings to disk.
    """
    names = []
    encodings = []
    for filepath in Path("face_recognizer/training").glob("*/*"):
        # print(filepath)
        name = filepath.parent.name
        image = face_recognition.load_image_file(filepath)
        face_locations = face_recognition.face_locations(image, model=model)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        for encoding in face_encodings:
            names.append(name)
            encodings.append(encoding)

    name_encodings = {"names": names, "encodings": encodings}
    with encodings_location.open(mode="wb") as f:
        pickle.dump(name_encodings, f)
    print(f"encodings saved {encodings_location}")


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
    model: str = "hog",
    encodings_location: Path = DEFAULT_ENCODINGS_PATH,
) -> None:
    """
    recognizes faces in images that don’t have a label
    """

    # load saved face encoding using pickl
    with encodings_location.open(mode="rb") as f:
        loaded_encodings = pickle.load(f)

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

    # use parallel iteration to match the face to encoding
    for bounding_box, unknown_encoding in zip(input_face_locations, input_face_encodings):
        name = _recognize_face(unknown_encoding, loaded_encodings)
        if not name:
            name = "Unknown"
        print(image_location, name, bounding_box)

if __name__ == "__main__":
    # create an encoding for images in training
    encode_known_faces()
    # recognize face in the validation folder
    # recognize_faces("face_recognizer/validation/anh2.jpg")
    # for filepath in Path("face_recognizer/validation").glob("*"):
    #     recognize_faces(filepath)
