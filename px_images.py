import configparser
import os

import cv2

from methods import mark_as_done


class PixelateImage:
    def __init__(self, config: configparser):
        self._images_folder = config["COMMON"]["images_path"]
        self._results_folder = config["COMMON"]["results_path"]

        # Desired "pixelated" size
        self._px_w = config["PARAMS"]["pixelated_width"]
        self._px_h = config["PARAMS"]["pixelated_high"]

        print("[INFO] - Pixel class created")

    def pixelate_image(self):
        for count, image_name in enumerate(os.listdir(self._images_folder)):

            if "DONE" in image_name:
                print("[WARN] - Ignoring {}".format(image_name))
            else:
                print("[INFO] - Pixelating {}".format(image_name))
                # Construct Image path
                image_path = "{}/{}".format(self._images_folder, image_name)

                # Read Image
                image = cv2.imread(image_path)

                # Get input size
                height, width = image.shape[:2]

                # Resize input to "pixelated" size
                temp = cv2.resize(image, (self._px_w, self._px_h), interpolation=cv2.INTER_LINEAR)

                # Initialize output image
                output = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)

                # Construct Output path
                output_path = "{}/results_{}.jpg".format(self._results_folder, count)

                # Save "pixelated" image
                cv2.imwrite(output_path, output)

                # Mark as done
                new_image_name = mark_as_done(image_path)
                os.rename(image_path, new_image_name)

        print('[INFO] - Finish pixelating')
