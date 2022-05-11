import configparser
import os.path

import cv2
import numpy as np

from methods import mark_as_done

global reference_point


def mouse_callback(event, x, y, flags, param):
    global reference_point
    if event == cv2.EVENT_LBUTTONDOWN:
        reference_point = (y, x)


class ColorImages:
    def __init__(self, config: configparser):
        self._image_folder = os.path.join(config["COMMON"]["images_path"], config["COMMON"]["color_images_path"])
        self._result_folder = os.path.join(config["COMMON"]["results_path"], config["COMMON"]["color_images_path"])

        self._image = config["LISTING"]["color_images_number"]

        self.lower_threshold = np.array([0, 0, 0])
        self.upper_threshold = np.array([255, 255, 255])

    def _set_lower_upper_hsv(self, image):
        global reference_point

        (y, x) = reference_point
        color_blue = image[y, x, 1]
        color_green = image[y, x, 1]
        color_red = image[y, x, 2]

        bgr_value = np.uint8([[[color_blue, color_green, color_red]]])
        hsv = cv2.cvtColor(bgr_value, cv2.COLOR_BGR2HSV)
        (h, s, v) = (hsv[0][0][0], hsv[0][0][1], hsv[0][0][2])
        self.lower_threshold = np.array([h - 50, s - 50, v - 50])
        self.upper_threshold = np.array([h + 50, s + 50, v + 50])

    def _set_threshold_hsv(self, image_path, save_results=False):
        global reference_point

        # read the image
        img = cv2.imread(image_path)

        cv2.namedWindow("Pick a Pixel", cv2.WINDOW_NORMAL)
        cv2.setMouseCallback("Pick a Pixel", mouse_callback)
        cv2.imshow("Pick a Pixel", img)

        if cv2.waitKey(0):
            cv2.destroyAllWindows()

        self._set_lower_upper_hsv(img)

        # img_blurred = cv2.GaussianBlur(img, (9, 9), cv2.BORDER_DEFAULT)

        # convert the BGR image to HSV colour space
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # create a mask for green colour using inRange function
        mask = cv2.inRange(hsv_img, self.lower_threshold, self.upper_threshold)

        # color transformation
        transformed_image = img.copy()
        transformed_image[mask > 0] = (0, 0, 255)

        # perform bitwise and on the original image arrays using the mask
        result = cv2.bitwise_and(img, img, mask=mask)

        # create resizable windows for displaying the images
        cv2.namedWindow("Original", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Transformed Image", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Mask", cv2.WINDOW_NORMAL)
        cv2.namedWindow("HSV", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Result", cv2.WINDOW_NORMAL)

        # display the images
        cv2.imshow("Original", img)
        cv2.imshow("Transformed Image", transformed_image)
        cv2.imshow("Mask", mask)
        cv2.imshow("HSV", hsv_img)
        cv2.imshow("Result", result)

        if cv2.waitKey(0):
            cv2.destroyAllWindows()

        if save_results:
            output_path_hsv = "{}/{}{}".format(self._result_folder, "HSV_", image_path.split("/")[-1])
            output_path_trans = "{}/{}{}".format(self._result_folder, "TRANSFORMED_", image_path.split("/")[-1])

            print("[INFO] - Saving HSV transformation for image {}".format(image_path.split("/")[-1]))
            cv2.imwrite(output_path_hsv, hsv_img)

            print("[INFO] - Saving MASKED transformation for image {}".format(image_path.split("/")[-1]))
            cv2.imwrite(output_path_trans, output_path_trans)


    def transform_color(self):

        for count, image_name in enumerate(os.listdir(self._image_folder)):

            if "DONE" in image_name:
                print("[WARN] - Ignoring {}".format(image_name))
            else:
                print("[INFO] - Changing color on image {}".format(image_name))

                # Construct image path
                image_path = os.path.join(self._image_folder, image_name)

                # Transforming image
                print("[INFO] - Transforming color on image {}".format(image_name))
                self._set_threshold_hsv(image_path, True)

                # Mark as done
                new_image_name = mark_as_done(image_path)
                os.rename(image_path, new_image_name)

        print("[INFO] - Finish with color transformation")
