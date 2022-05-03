import configparser
import cv2
import numpy as np

global reference_point


def mouse_callback(event, x, y, flags, param):
    global reference_point
    if event == cv2.EVENT_LBUTTONDOWN:
        reference_point = (y, x)


class ColorImages:
    def __init__(self, config: configparser):
        self._images_folder = config["COMMON"]["images_path"]
        self._results_folder = config["COMMON"]["results_path"]

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
        self.lower_threshold = np.array([h-50, s-50, v-50])
        self.upper_threshold = np.array([h+50, s+50, v+50])

    def filter_hsv(self):
        global reference_point

        # read the image
        img = cv2.imread("images/image_8.jpg")

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
        res = cv2.bitwise_and(img, img, mask=mask)

        # create resizable windows for displaying the images
        cv2.namedWindow("original", cv2.WINDOW_NORMAL)
        cv2.namedWindow("transformed image", cv2.WINDOW_NORMAL)
        cv2.namedWindow("mask", cv2.WINDOW_NORMAL)
        cv2.namedWindow("hsv", cv2.WINDOW_NORMAL)
        cv2.namedWindow("res", cv2.WINDOW_NORMAL)

        # display the images
        cv2.imshow("original", img)
        cv2.imshow("transformed image", transformed_image)
        cv2.imshow("mask", mask)
        cv2.imshow("hsv", hsv_img)
        cv2.imshow("res", res)

        if cv2.waitKey(0):
            cv2.destroyAllWindows()
