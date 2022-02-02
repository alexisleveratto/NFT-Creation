import os


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
