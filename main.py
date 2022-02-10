import configparser

from transformation.px_images import PixelateImage
from transformation.colour_images import ColorImages
from methods import mark_as_undone, normalize_images_name, save_results, create_directory

CONFIG_FILE_PATH = "resources/application.properties"

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)

    if config.getboolean("RUNNING", "check_directories"):
        create_directory(config["COMMON"]["images_path"])
        create_directory(config["COMMON"]["results_path"])
        create_directory(config["COMMON"]["saved_path"])

    if config.getboolean("RUNNING", "normalize_images_name"):
        print("[INFO] - Normalizing images")
        normalize_images_name(config["COMMON"]["images_path"])

    if config.getboolean("RUNNING", "pixelate_image"):
        print("[INFO] - Pixelating images")
        pixelator = PixelateImage(config)
        pixelator.pixelate_image()

    colorator = ColorImages(config)
    colorator.filter_green()


    if config.getboolean("RUNNING", "mark_undo"):
        print("[INFO] - Marking as undo")
        mark_as_undone(config["COMMON"]["images_path"], config["LISTING"]["images_number"])

    if config.getboolean("RUNNING", "save_results"):
        print("[INFO] - Saving images")
        save_results(config["COMMON"]["results_path"], config["COMMON"]["saved_path"], config["LISTING"]["save_this"])
