import configparser

from px_images import PixelateImage

CONFIG_FILE_PATH = "resources/application.properties"

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)

    parser = PixelateImage(config)
    parser.pixelate_image()



