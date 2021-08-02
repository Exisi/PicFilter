import imghdr
from PIL import Image
import hashlib


def is_img(f):
    # 判断文件是否为图片
    '''
    :param f: 图片路径
    :param imgType_list: 图片格式
    :return: bool
    '''
    imgType_list = {'jpg', 'bmp', 'png', 'jpeg', 'rgb', 'tif', 'gif', 'webp'}
    if imghdr.what(f) in imgType_list:
        return True
    else:
        return False


def wh_type(f):
    # 判断图片是横屏还是竖屏
    '''
    :param f: 图片路径
    :return: bool
    '''
    im = Image.open(f)
    if im.width > im.height:  # 横屏
        return True
    else:  # 竖屏
        return False


def hist(f):
    im=Image.open(f)
    size=10,10  #不建议调低，容易误判，大小像素最低值5
    i=im.resize(size, Image.ANTIALIAS).convert('RGB')
    return i.histogram()
