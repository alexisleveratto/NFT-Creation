import configparser
import os.path

import cv2
import numpy as np


class MixImage:
    def __init__(self, config: configparser):
        self.foreground_image_path = os.path.join(
            config["COMMON"]["images_path"], config["MIX"]["foreground_image_path"]
        )
        self.background_image_path = os.path.join(
            config["COMMON"]["images_path"], config["MIX"]["background_image_path"]
        )

        self.color_threshold = eval(config["COLOR"]["color_threshold"])

        self.mixed_image_path = os.path.join(
            config["MIX"]["mix_image_path"], self.foreground_image_path.split("/")[-1]
        )

        self._set_lower_upper_fixed()

    def _set_lower_upper_fixed(self):
        self.lower_threshold = np.array(
            [
                self.color_threshold[0] - 70,
                self.color_threshold[1] - 70,
                self.color_threshold[2] - 70,
            ]
        )
        self.upper_threshold = np.array(
            [
                self.color_threshold[0] + 70,
                self.color_threshold[1] + 70,
                self.color_threshold[2] + 70,
            ]
        )

    def mix_it(self, save_result: bool = True, see_result: bool = False):
        foreground_image = cv2.imread(self.foreground_image_path)
        background_image = cv2.imread(self.background_image_path)

        hsv_img = cv2.cvtColor(foreground_image, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv_img, self.lower_threshold, self.upper_threshold)

        # Get input size
        new_height, new_width = foreground_image.shape[:2]

        # Resize input to "pixelated" size
        new_back_image = cv2.resize(
            background_image, (new_width, new_height), interpolation=cv2.INTER_LINEAR
        )

        transformed_image = foreground_image.copy()
        transformed_image[mask > 0] = new_back_image[mask > 0]

        if see_result:
            cv2.namedWindow("Mixed Result", cv2.WINDOW_NORMAL)
            cv2.imshow("Mixed Result", transformed_image)

            if cv2.waitKey(0):
                cv2.destroyAllWindows()

        if save_result:
            cv2.imwrite(self.mixed_image_path, transformed_image)
