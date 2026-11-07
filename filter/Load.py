import os
import shutil

from utils import I18n


def create_folder(output_path: str):
    # Create the output directory
    if not exists(output_path): os.makedirs(output_path)


def read(file_dir):
    '''
    Get all file paths under the directory
    :param file_list: list of file paths
    :return List
    '''
    file_list = []
    for root, dirs, files in os.walk(file_dir):  # separate directories and files
        for f in files:  # collect each file
            file_list.append(os.path.join(root, f))
    return file_list


def full_copy(file_path, file_output: str):
    '''
    Copy the image into the matched-image folder under the output directory
    :param file_path: image path
    :param file_output: image output path
    :param file_name: image name
    '''
    file_name = name(file_path)
    if not exists(file_output + '/' + I18n.tr('folder.matched')):
        os.makedirs(file_output + '/' + I18n.tr('folder.matched'))
    shutil.copyfile(file_path, file_output + '/' + I18n.tr('folder.matched') + '/' + file_name)


def _copy(file_path, file_output: str):
    '''
    Copy the image into the output directory
    :param file_path: image path
    :param file_output: image output path
    :param file_name: image name
    '''
    file_name = name(file_path)
    if not exists(file_output): os.makedirs(file_output)
    shutil.copyfile(file_path, file_output + file_name)


def copy(file_path, file_output: str, im_type: int):
    '''
    Copy the image into its type folder
    :param file_path: image path
    :param file_output: image output path
    :param file_name: image name
    '''
    file_name = name(file_path)
    folder = I18n.type_folder(im_type)
    if exists(file_output + '/' + folder):
        shutil.copyfile(file_path, file_output + '/' + folder + '/' + file_name)


def name(file_path: str):
    # Get the image file name
    return os.path.basename(file_path)


def suffix(file_path: str):
    # Get the image file extension
    suffix = os.path.splitext(file_path);
    return suffix[1]


def exists(file_dir: str):
    # Check whether the path exists
    return os.path.exists(file_dir)


def delete(f):
    # Delete the image file
    os.remove(f)
