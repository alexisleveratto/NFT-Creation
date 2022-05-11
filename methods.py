import os


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
    undo_images_list = ["DONE_image_{}.jpg".format(img_number) for img_number in image_numbers.split(",")]
    done_images = [image_name for image_name in os.listdir(images_path) if "DONE_" in image_name]

    to_change_name = ["{}/{}".format(images_path, img_name) for img_name in undo_images_list if img_name in done_images]
    for img_to_change in to_change_name:
        img_changed = img_to_change.replace("DONE_", "")
        os.rename(img_to_change, img_changed)


def save_results(result_image_path: str, save_image_path: str, image_numbers: str):
    save_images_list = ["results_{}.jpg".format(img_number) for img_number in image_numbers.split(",")]

    results_to_save = ["{}/{}".format(result_image_path, save_img) for save_img in save_images_list if
                       save_img in os.listdir(result_image_path)]

    for img_to_save in results_to_save:
        new_directory = "{}/{}".format(save_image_path, img_to_save.split("/")[-1])
        os.replace(img_to_save, new_directory)
