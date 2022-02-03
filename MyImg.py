import imghdr
from PIL import Image


def is_img(f):
    '''
    判断文件是否为图片
    :param f: 图片路径
    :param imgType_list: 图片格式
    :return: bool
    '''
    imgType_list = {'jpg', 'bmp', 'png', 'jpeg', 'rgb', 'tif', 'gif', 'webp'}  # 其他特殊格式课自行添加
    if imghdr.what(f) in imgType_list:
        return True
    else:
        return False


def wh_type(f):
    '''
    判断图片类型
    :param f: 图片路径
    :return: int
    '''
    im = Image.open(f)
    if im.width == im.height:  # 方图
        return 0
    elif im.width > im.height:  # 横图
        return 1
    elif im.width < im.height:  # 竖图
        return 2
    else:  # 未知
        return 3


def hist(f):
    '''
    图片像素直方图
    :param f: 图片路径
    :return: List
    '''
    im = Image.open(f)
    return im.histogram()


def wh_limitByPor(f, max_scale: float, min_scale: float):
    '''
    根据长宽比例限制
    :param f: 图片路径
    :param type: 图片类型
    :param max_scale,min_scale: 最大/最小宽高比例
    :return: bool
    '''
    im = Image.open(f)
    w = float(im.width)
    h = float(im.height)
    if max_scale >= (w / h) >= min_scale or max_scale >= float(h / w) >= min_scale:
        return True
    else:
        return False


def wh_limitByWH(f, limit: dict):
    '''
    根据纯数字宽高限制
    :param f: 图片路径
    :param limit: 最大最小宽高限制
    :return: bool
    '''
    im = Image.open(f)
    w = float(im.width)
    h = float(im.height)
    if float(limit['maxW'].get()) >= w >= float(limit['minW'].get()) and float(limit['maxH'].get()) >= h >= float(
            limit['minH'].get()):
        return True
    else:
        return False
