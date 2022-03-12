import os
import shutil


def create_folder(output_path: str):
    # 创建输出目录
    if not exists(output_path): os.makedirs(output_path)


def read(file_dir):
    '''
    获取图片路径
    :param file_list: 图片路径列表
    :return List
    '''
    file_list = []
    for root, dirs, files in os.walk(file_dir):  # 取出目录和文件
        for f in files:  # 迭代获取文件
            file_list.append(os.path.join(root, f))
    return file_list


def full_copy(file_path, file_output: str):
    '''
    复制图片到对应文件
    :param file_path: 图片路径
    :param file_output: 图片输出路径
    :param file_name: 图片名称
    '''
    file_name = name(file_path)
    if not exists(file_output + '/符合的图片'): os.makedirs(file_output + '/符合的图片')
    shutil.copyfile(file_path, file_output + "/符合的图片/" + file_name)


def copy(file_path, file_output: str, im_type: int):
    '''
    复制图片分类到对应文件
    :param file_path: 图片路径
    :param file_output: 图片输出路径
    :param file_name: 图片名称
    '''
    file_name = name(file_path)
    if im_type == 0:
        if exists(file_output + '/方图'): shutil.copyfile(file_path, file_output + '/方图/' + file_name)
    elif im_type == 1:
        if exists(file_output + '/横图'): shutil.copyfile(file_path, file_output + '/横图/' + file_name)
    elif im_type == 2:
        if exists(file_output + '/竖图'): shutil.copyfile(file_path, file_output + '/竖图/' + file_name)


def name(file_path: str):
    # 获取图片文件名
    return os.path.basename(file_path)


def suffix(file_path: str):
    # 获取图片文件后缀
    suffix = os.path.splitext(file_path);
    return suffix[1]


def exists(file_dir: str):
    # 路径是否存在
    return os.path.exists(file_dir)


def delete(f):
    # 图片删除
    os.remove(f)
