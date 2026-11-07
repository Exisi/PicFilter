from PIL import Image


def is_img(f):
    '''
    Check whether the file is an image based on its content
    :param f: image path
    :return: bool
    '''
    try:
        with Image.open(f) as im:
            return im.format is not None
    except (OSError, SyntaxError, ValueError, Image.DecompressionBombError):
        return False


def wh_type(f):
    '''
    Determine the image type
    :param f: image path
    :return: int
    '''
    im = Image.open(f)
    if im.width == im.height:  # square
        return 0
    elif im.width > im.height:  # landscape
        return 1
    elif im.width < im.height:  # portrait
        return 2
    else:  # unknown
        return 3


def hist(f):
    '''
    Image pixel histogram
    :param f: image path
    :return: List
    '''
    im = Image.open(f)
    return im.histogram()


def wh_limitByPor(f, max_scale: float, min_scale: float):
    '''
    Filter by aspect ratio
    :param f: image path
    :param type: image type
    :param max_scale,min_scale: maximum/minimum aspect ratio
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
    Filter by exact width and height limits
    :param f: image path
    :param limit: maximum/minimum width and height limits (numeric values, not Tk variables)
    :return: bool
    '''
    im = Image.open(f)
    w = float(im.width)
    h = float(im.height)
    if limit['maxW'] >= w >= limit['minW'] and limit['maxH'] >= h >= limit['minH']:
        return True
    else:
        return False
