import os

import numpy as np
import cv2


def create_directory(directory_path):
    if not (os.path.isdir(directory_path)):
        os.mkdir(directory_path)


def normalize_images_name(images_path: str):
    for count, filename in enumerate(os.listdir(images_path)):
        dst = "{}/image_{}.jpg".format(images_path, count)
        src = "{}/{}".format(images_path, filename)

        # ToDo : Check if filename already exists in destination folder
        os.rename(src, dst)


def mark_as_done(image_path: str):
    path_list = image_path.split("/")
    image_new_name = "DONE_{}".format(path_list.pop())
    path_list.append(image_new_name)

    return "/".join(path_list)


def mark_as_undone(images_path: str, image_numbers: str):
    undo_images_list = [
        "DONE_image_{}.jpg".format(img_number)
        for img_number in image_numbers.split(",")
    ]
    done_images = [
        image_name for image_name in os.listdir(images_path) if "DONE_" in image_name
    ]

    to_change_name = [
        "{}/{}".format(images_path, img_name)
        for img_name in undo_images_list
        if img_name in done_images
    ]
    for img_to_change in to_change_name:
        img_changed = img_to_change.replace("DONE_", "")
        os.rename(img_to_change, img_changed)


def save_results(result_image_path: str, save_image_path: str, image_numbers: str):
    save_images_list = [
        "results_{}.jpg".format(img_number) for img_number in image_numbers.split(",")
    ]

    results_to_save = [
        "{}/{}".format(result_image_path, save_img)
        for save_img in save_images_list
        if save_img in os.listdir(result_image_path)
    ]

    for img_to_save in results_to_save:
        new_directory = "{}/{}".format(save_image_path, img_to_save.split("/")[-1])
        os.replace(img_to_save, new_directory)


def list_files(base_path: str, valid_ext=[]):
    image_types = tuple([".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"] + valid_ext)

    # loop over the directory structure
    for (rootDir, dirNames, filenames) in os.walk(base_path):
        # loop over the filenames in the current directory
        for filename in filenames:
            # determine the file extension of the current file
            ext = filename[filename.rfind(".") :].lower()

            # check to see if the file is an image and should be processed
            if ext.endswith(image_types):
                # construct the path to the image and yield it
                image_path = os.path.join(rootDir, filename)
                yield image_path


def svg_2_image(base_path: str, target_path: str):
    # ToDo - this does not work
    pass


def centroid_histogram(clt):
    # grab the number of different clusters and create a histogram
    # based on the number of pixels assigned to each cluster
    num_labels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=num_labels)

    # normalize the histogram, such that it sums to one
    hist = hist.astype("float")
    hist /= hist.sum()

    # return the histogram
    return hist


def plot_colors(hist, centroids):
    # initialize the bar chart representing the relative frequency
    # of each of the colors
    bar = np.zeros((50, 300, 3), dtype="uint8")
    start_x = 0
    # loop over the percentage of each cluster and the color of
    # each cluster
    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        end_x = start_x + (percent * 300)
        cv2.rectangle(
            bar, (int(start_x), 0), (int(end_x), 50), color.astype("uint8").tolist(), -1
        )
        start_x = end_x

    # return the bar chart
    return bar


def move_image(source_path: str, target_path: str):
    create_directory(target_path)
    image_name = source_path.split("/")[-1]

    os.rename(source_path, os.path.join(target_path, image_name))
