import configparser
import cv2
import numpy as np


class ColorImages:
    def __init__(self, config: configparser):
        self._images_folder = config["COMMON"]["images_path"]
        self._results_folder = config["COMMON"]["results_path"]

        self.lower_green = np.array([500, 100, 50])
        self.upper_green = np.array([70, 255, 255])

    def filter_green(self):
        # read the image
        img = cv2.imread("D:/NFT-Creation/images/image_8.jpg")

        # convert the BGR image to HSV colour space
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # create a mask for green colour using inRange function
        mask = cv2.inRange(hsv_img, self.lower_green, self.upper_green)

        # perform bitwise and on the original image arrays using the mask
        res = cv2.bitwise_and(img, img, mask=mask)

        # create resizable windows for displaying the images
        cv2.namedWindow("original", cv2.WINDOW_NORMAL)
        cv2.namedWindow("res", cv2.WINDOW_NORMAL)
        cv2.namedWindow("hsv", cv2.WINDOW_NORMAL)
        cv2.namedWindow("mask", cv2.WINDOW_NORMAL)

        # display the images
        cv2.imshow("original", img)
        cv2.imshow("mask", mask)
        cv2.imshow("hsv", hsv_img)
        cv2.imshow("res", res)

        if cv2.waitKey(0):
            cv2.destroyAllWindows()






