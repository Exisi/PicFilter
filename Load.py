import os
import shutil


def create_folder(output_path: str):
    # 创建输出目录
    if not exists(output_path + '/横图'): os.makedirs(output_path + '/横图')
    if not exists(output_path + '/竖图'): os.makedirs(output_path + '/竖图')
    if not exists(output_path + '/方图'): os.makedirs(output_path + '/方图')


def read(file_dir):
    # 获取图片路径
    '''
    :param file_list: 图片路径列表
    :return List
    '''
    file_list = []
    for root, dirs, files in os.walk(file_dir):  # 取出目录和文件
        file_list = [os.path.join(root, f) for f in files]  # 迭代获取文件
    return file_list


def copy(file_path, file_output: str, mode: int):
    # 复制图片到对应文件
    '''
    :param file_path: 图片路径
    :param file_output: 图片输出路径
    :param file_name: 图片名称
    :return: bool 
    '''
    file_name = name(file_path)
    if mode == 1:
        shutil.copyfile(file_path, file_output + '/横图/' + file_name)
    elif mode == 2:
        shutil.copyfile(file_path, file_output + '/竖图/' + file_name)
    else:
        shutil.copyfile(file_path, file_output + '/方图/' + file_name)


def name(file_path: str):
    # 获取图片文件名
    return os.path.basename(file_path)


def exists(file_dir: str):
    # 路径是否存在
    return os.path.exists(file_dir)


def delete(f):
    # 图片删除
    os.remove(f)


def get_size(f):
    # 获取文件大小
    return os.path.getsize(f)


def move(f):
    # 文件移动
    filename = name(f)
    path = os.path.dirname(os.path.dirname(f))
    if not exists(path + '/已移除的图片'): os.makedirs(path + '/已移除的图片')
    shutil.move(f, path + '/已移除的图片/' + filename)
