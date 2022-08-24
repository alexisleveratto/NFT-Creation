import configparser

from imutils import paths
import face_recognition
import pickle
import cv2
import os


class FaceEncoder:
    def __init__(self, config: configparser):
        self._dataset = config["FACES"]["dataset"]
        self._encodings = config["FACES"]["encodings"]
        self._detection_method = config["FACES"]["detection_method"]

        self._imagePaths = list(paths.list_images(self._dataset))

        # initialize the list of known encodings and known names
        self._knownEncodings = []
        self._knownNames = []

    def encode_faces(self):
        # loop over the images path
        for (i, imagePath) in enumerate(self._imagePaths):
            # extract the person name from the image path
            print("[INFO] provessing image {}/{}".format(i + 1, len(self._imagePaths)))

            name = imagePath.split(os.path.sep)[-2]

            # load the input image and convert it from BGR (OpenCV ordering) to dlib ordering (RGB)
            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # but the dlib actually expects RGB

            # detect the (x, y)-coordinates of the bounding boxes corresponding to each face in the input image
            boxes = face_recognition.face_locations(rgb, model=self._detection_method)

            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, boxes)

            # loop over the encodings
            for encoding in encodings:
                # add each encoding + name to our set of known names and encodings
                self._knownEncodings.append(encoding)
                self._knownNames.append(name)

        # dump the facial encodings + names to disk
        print("[INFO] serializing encodings...")
        data = {"encodings": self._knownEncodings, "names": self._knownNames}
        f = open(self._encodings, "wb")
        f.write(pickle.dumps(data))
        f.close()

