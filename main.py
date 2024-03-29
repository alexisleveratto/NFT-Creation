import configparser

from transformation.px_images import PixelateImage
from transformation.colour_images import ColorImages
from transformation.mix_images import MixImage
from scrape_images import WebScrape
from findfaces.encode_faces import FaceEncoder
from findfaces.recognize_faces import FaceJudge
from findfaces.face_replacement import FaceReplacement
from methods import (
    mark_as_undone,
    normalize_images_name,
    save_results,
    create_directory,
    svg_2_image,
)

CONFIG_FILE_PATH = "resources/application.properties"

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    if config.getboolean("FACES", "encode_faces"):
        encoder = FaceEncoder(config)
        encoder.encode_faces()

    if config.getboolean("FACES", "recognize_faces"):
        judge = FaceJudge(config)
        judge.recognize_face_image()

    if config.getboolean("RUNNING", "work_with_faces"):
        faceReplacement = FaceReplacement(config)
        if config.getboolean("FACES", "replace_faces"):
            faceReplacement.replace_face()

        if config.getboolean("FACES", "check_two_faces"):
            faceReplacement.move_images_two_faces()

        if config.getboolean("FACES", "qr_2_png"):
            svg_2_image(
                base_path=config["FACES"]["qr_svg"],
                target_path=config["FACES"]["qr_images"],
            )

    if config.getboolean("WEB", "scrape_4_images"):
        spiderWeb = WebScrape(config)
        spiderWeb.download("marilyn", "monroe")

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
            print(
                "[INFO] - Bad color transformation request (options: BULK, UNIQUE, ALEATORY, EXPLORATORY)"
            )

    if config.getboolean("RUNNING", "mix_it_up"):
        mixator = MixImage(config)
        mixator.mix_it(True, False)
