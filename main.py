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

    if config.getboolean("RUNNING", "color_change"):
        print("[INFO] - Change color")
        what_kind_of_transformation = config["COLOR"]["what_color_change"].upper()
        if what_kind_of_transformation == "BULK":
            colorator = ColorImages(config)
            colorator.bulk_transform()
        elif what_kind_of_transformation == "UNIQUE":
            colorator = ColorImages(config)
            colorator.transform()
        elif what_kind_of_transformation == "ALEATORY":
            colorator = ColorImages(config)
            colorator.aleatory_mask_transformation()
        elif what_kind_of_transformation == "EXPLORATORY":
            colorator = ColorImages(config)
            colorator.set_analyze_threshold_hsv(config["COLOR"]["image_to_explore"])
        else:
            print("[INFO] - Bad color transformation request (options: BULK, UNIQUE, ALEATORY, EXPLORATORY)")

    if config.getboolean("RUNNING", "mark_undo"):
        print("[INFO] - Marking as undo")
        mark_as_undone(config["COMMON"]["images_path"], config["LISTING"]["images_number"])

    if config.getboolean("RUNNING", "save_results"):
        print("[INFO] - Saving images")
        save_results(config["COMMON"]["results_path"], config["COMMON"]["saved_path"], config["LISTING"]["save_this"])
