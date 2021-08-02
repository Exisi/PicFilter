import os
import shutil


def create_folder(output_path: str):
    # 创建横竖屏文件夹
    if not exists(output_path + '/横屏'): os.makedirs(output_path + '/横屏')
    if not exists(output_path + '/竖屏'): os.makedirs(output_path + '/竖屏')


def read(file_dir):
    # 获取图片路径
    '''
    :param file_dir: 图片目录
    :param file_list: 图片路径列表
    :param f: 图片路径
    :return List
    '''
    file_list = []
    if os.path.exists(file_dir):
        # 取出目录和文件
        for root, dirs, files in os.walk(file_dir):
            for f in files:  # 迭代文件
                for r in root.splitlines():  # 迭代目录
                    if exists(os.path.join(r, f)):  # 猜测路径，逐个匹配
                        file_list.append(os.path.join(r, f))  # 取出匹配路径
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
    if mode > 0:
        shutil.copyfile(file_path, file_output + '/横屏/' + file_name)
    else:
        shutil.copyfile(file_path, file_output + '/竖屏/' + file_name)


def name(file_path):
    # 获取图片文件名
    '''
    :param file_path: 图片路径
    :return: str
    '''
    return os.path.basename(file_path)


def exists(file_dir):
    # 路径是否存在
    """
    :param file_dir: 文件夹路径
    :return: bool
    """
    return os.path.exists(file_dir)


def delete(f):
    os.remove(f)
