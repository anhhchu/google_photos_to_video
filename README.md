# Create video from your own images download from Google Photos

### Step 1: Set up Google Photos API
Follow this [repo](https://github.com/polzerdo55862/google-photos-api/blob/main/Google_API.ipynb) to set up the virtualenv and Authenticate to Google Photos API

### Step 2 (optional): Detect your images using face-recognition

```bash
face_recognizer: directory for face recognition
-- output: save the encodings.pkl file 
-- training: images for training
--- person1: dir of person1's images
----- person1_1.jpg
----- person1_2.jpg
--- person2: dir of person2's images
----- person2_1.jpg
----- person2_2.jpg
-- validation: images for validate, a few images of each person, and images of unknown person
----- person1_validate_1.jpg
----- person2_validate_2.jpg
----- unknown_person.jpg
```

* Add your images to training folder
* Run `./face_recognizer/detector.py` to generate the new model encoding with your own images. 
* The encodings.pkl pickle file save to `./face_recognizer/output/encodings.pkl`

### Step 3: Run `app.py --date_str <yyyy-mm-dd> --person <person_name>` to call main function 

`app.py` will do 3 things

* Download images for a specified date_str by calling `download_image.py` to `./downloads/{date_str}`
* Process images, keep images of the target person, padding the images to 1920x1080 pixels and save to `./downloads/target/{date_str}` dir
* Create video from the processed images and audio from `./audio` and save to `./output_videos`


### License
[MIT](https://choosealicense.com/licenses/mit/)