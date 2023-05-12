import configparser
import os.path

import cv2
from imutils import paths
from methods import (
    list_files,
    create_directory,
    centroid_histogram,
    plot_colors,
    move_image,
)
from sklearn.cluster import KMeans

import numpy as np

from findfaces.recognize_faces import FaceJudge


class FaceReplacement:
    def __init__(self, config: configparser):
        self._dataset = config["FACES"]["new_images"]
        self._imagePaths = list(paths.list_images(self._dataset))
        self._qrPaths = list(list_files(config["FACES"]["qr_images"], [".svg"]))
        self._resultPaths = config["FACES"]["result_path"]

        self._checkMoreThanOneFaceImg = config.getboolean("FACES", "more_faces")
        self._reorderPath = config["FACES"]["reorder_path"]

        create_directory(self._resultPaths)

        self._faceJudge = FaceJudge(config)

    def _change_qr_colors(self, qr_image, black_replacement, white_replacement):
        rows, columns, _ = qr_image.shape
        for i in range(rows):
            for j in range(columns):
                if np.all(qr_image[i, j] == (255, 255, 255)):
                    qr_image[i, j] = white_replacement
                else:
                    qr_image[i, j] = black_replacement
        return qr_image

    def _colored_qr(
        self, qr_image, roi_image, n_colors: int = 2, show_images: bool = False
    ):
        # reshape the image to be a list of pixels
        image = roi_image.reshape((roi_image.shape[0] * roi_image.shape[1], 3))

        clt = KMeans(n_clusters=n_colors)
        clt.fit(image)

        hist = centroid_histogram(clt)
        bar = plot_colors(hist, clt.cluster_centers_)

        sorted_colors = np.unique(bar[0], return_counts=True, axis=0)

        colors = sorted_colors[0]
        counts = sorted_colors[1]

        if counts[0] > counts[1]:
            dominant_color = colors[0]
            secondary_color = colors[1]
        else:
            dominant_color = colors[1]
            secondary_color = colors[0]

        qr_colored = self._change_qr_colors(qr_image, dominant_color, secondary_color)

        if show_images:
            cv2.imshow("QR_COLORED", qr_colored)
            cv2.imshow("ROI", roi_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return qr_colored

    def move_images_two_faces(self):
        for image_path in self._imagePaths:
            image = cv2.imread(image_path)
            boxes, _ = self._faceJudge.recognize_face_image(image)

            if len(boxes) != 1:
                print("[WARN] - More than one face found in {}".format(image_path))
                move_image(image_path, self._reorderPath)

    def replace_face(self, show_results: bool = False):
        for (i, qrPath) in enumerate(self._qrPaths):
            print("[INFO] Replacing for qr {}/{}".format(i + 1, len(self._qrPaths)))
            print("[INFO] Image {}".format(self._imagePaths[i]))

            qr_image = cv2.imread(qrPath)

            image = cv2.imread(self._imagePaths[i])

            model_name = self._imagePaths[i].split(os.path.sep)[-2]

            boxes, encoded_names = self._faceJudge.recognize_face_image(image)

            if (len(boxes) != 1) and self._checkMoreThanOneFaceImg:
                print(
                    "[WARN] - More than one face found in {}".format(
                        self._imagePaths[i].split("/")[-1]
                    )
                )
                move_image(self._imagePaths[i], self._reorderPath)
                continue

            for (n, encoded_name) in enumerate(encoded_names):
                if (
                    True
                ):  # Todo:  SOLVE THIS FOR WHEN THE PICTURE HAS MORE THAN ONE FACE (encoded_name == model_name:)
                    #        we just want to replace one marilyn face
                    (top, right, bottom, left) = boxes[n]
                    break

            roi = image[top:bottom, left:right]

            # roi and qr_image should have the same size
            new_size = (right - left, bottom - top)
            qr_image_resized = cv2.resize(
                qr_image, new_size, interpolation=cv2.INTER_LINEAR
            )

            # change qr image color
            print("[INFO] - Changing qr color")
            qr_image_colored = self._colored_qr(qr_image_resized, roi)

            # Now create a mask of logo and create its inverse mask also
            qr_image_gray = cv2.cvtColor(qr_image_colored, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(qr_image_gray, 10, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)

            # Take only region of logo from logo image
            qr_image_fg = cv2.bitwise_and(qr_image_colored, qr_image_colored, mask=mask)

            # Now black-out the area of logo in ROI
            image_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

            # Put logo in ROI and modify the main image
            dst = cv2.add(image_bg, qr_image_fg)
            image[top:bottom, left:right] = dst

            image_name = qrPath.split("/")[-1]
            image_path = os.path.join(self._resultPaths, image_name)
            cv2.imwrite(image_path, image)

            if show_results:
                cv2.imshow("Image Result", image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
