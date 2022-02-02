import configparser
import os

config = configparser.ConfigParser()
config.read("resources/application.properties")


def rename_images():
    images_path = config["COMMON"]["image_path"]

    for count, filename in enumerate(os.listdir(images_path)):
        dst = "{}/image_{}.jpg".format(images_path, count)
        src = "{}/{}".format(images_path, filename)

        # ToDo : Check if filename already exists in destination folder
        os.rename(src, dst)



