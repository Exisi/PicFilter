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
    # 判断图片类型
    im = Image.open(f)
    if im.width > im.height:  # 横图
        return 1
    elif im.width < im.height:  # 竖图
        return 2
    else:  # 方图
        return 0


def hist(f):
    '''
    图片像素直方图
    :param f: 图片路径
    :param size: 图片重设的大小，减小像素计算量
    :return: Pil.im.histogram 图片的像素直方图
    '''
    im = Image.open(f)
    size = 10, 10  # 不建议调低，容易误判，大小像素最低值5
    i = im.resize(size, Image.ANTIALIAS).convert('P')
    return i.histogram()


def wh_limitByPor(f, type: str, proprotion: float):
    '''
    根据长宽比例限制
    :param f: 图片路径
    :param type: 图片类型
    :param proprotion: 宽高比例
    :return: bool
    '''
    im = Image.open(f)
    w = im.width
    h = im.height
    print('w:', w, 'h:', h, w / h, 'type', type)
    if type == '1' and (h / w) > proprotion:
        return True
    elif type == '2' and (w / h) > proprotion:
        return True
    else:
        return False


def wh_limitByWH(f, limit: dict, type: str):
    '''
    根据纯数字宽高限制
    :param f: 图片路径
    :param limit: 最大最小宽高限制
    :param type: 图片类型
    :return: bool
    '''
    im = Image.open(f)
    w = im.width
    h = im.height
    if type == '1':
        if h < limit['maxH']: return True
    elif type == '2':
        if w < limit['maxW']: return True
    else:
        if w <= limit['maxW'] and w >= limit['minW'] and h <= limit['maxH'] and h >= limit['minH']: return True
    return False
