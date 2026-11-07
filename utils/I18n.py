"""Runtime translation support for the Chinese and English interface."""

import json
import os
import tempfile

DEFAULT_LANGUAGE = 'zh'
LANGUAGE_LABELS = {'zh': '中文', 'en': 'English'}

TRANSLATIONS = {
    'zh': {
        'nav.duplicate': '图片去重',
        'nav.ratio': '比例限制',
        'nav.size': '宽高限制',
        'nav.classify': '图片分类',
        'nav.collection': '集合选区',
        'nav.about': '关于',
        'app.version': '版本 {version}',
        'sidebar.language': '语言',
        'sidebar.appearance': '外观',
        'theme.system': '跟随系统',
        'theme.light': '浅色',
        'theme.dark': '深色',
        'button.browse': '浏览',
        'button.start': '开始处理',
        'status.ready': '就绪',
        'label.input_dir': '输入目录',
        'label.output_dir': '输出目录',
        'label.left_input_dir': '左输入目录',
        'label.right_input_dir': '右输入目录',
        'label.image_type': '图片类型',
        'label.min_ratio': '最小比例',
        'label.max_ratio': '最大比例',
        'label.min_width': '最小宽度',
        'label.max_width': '最大宽度',
        'label.min_height': '最小高度',
        'label.max_height': '最大高度',
        'image_type.all': '全部',
        'image_type.horizontal': '横图',
        'image_type.vertical': '竖图',
        'image_type.square': '方图',
        'tip.prefix': '提示',
        'tip.duplicate': '图片去重会直接删除重复的图片，操作前请先备份重要文件。',
        'tip.ratio': '按图片长宽比例筛选，符合的图片会复制到输出目录。',
        'tip.size': '按图片宽高像素范围筛选，符合的图片会复制到输出目录。',
        'tip.classify': '按横图 / 竖图 / 方图对图片进行分类。',
        'tip.collection': '对两组图片做交集 / 差集，结果会复制到输出目录。',
        'collection.intersection': '交集',
        'collection.left_diff': '左差集',
        'collection.right_diff': '右差集',
        'collection.symmetric_diff': '对称差集',
        'about.description': '一个基于 Pillow 的批量图片筛选工具，适用于整理大量图片。',
        'about.feature.duplicate': '图片去重',
        'about.feature.ratio': '长宽比例筛选',
        'about.feature.size': '宽高像素筛选',
        'about.feature.classify': '横 / 竖 / 方图分类',
        'about.feature.collection': '两组图片的集合对比',
        'about.project': '项目地址',
        'about.checking': '正在检查更新…',
        'about.up_to_date': '已是最新版本',
        'about.update_available': '发现新版本 {version}',
        'about.check_failed': '检查更新失败，请稍后重试',
        'error.title.input': '输入错误',
        'error.title.selection': '选择错误',
        'error.path_missing': '文件路径不存在，请重新选择！',
        'error.same_in_out': '文件输入路径与输出路径不能相同，请重新选择！',
        'error.left_same_out': '文件左输入路径和输出路径不能相同，请重新选择！',
        'error.right_same_out': '文件右输入路径和输出路径不能相同，请重新选择！',
        'error.left_same_right': '文件左输入路径和右输入路径不能相同，请重新选择！',
        'error.ratio_empty': '长宽比不能为空！',
        'error.ratio_order': '最大长宽比不能小于最小长宽比！',
        'error.value_empty': '输入内容不能为空！',
        'error.limit_order': '最大值不能小于最小值！',
        'error.too_large': '数值过大！',
        'error.positive_integer': '输入内容必须为正整数数字！',
        'error.select_type': '请至少选择一种图片类型！',
        'error.select_set': '请至少选择一种集合区间！',
        'validation.positive_integer': '请输入正整数数字！',
        'validation.number': '请输入有效数字！',
        'log.duplicate_deleted': '[ {name} ] - 重复，已删除\n\n',
        'log.no_duplicate': '无重复，下一张\n\n',
        'log.matched': '[ {name} ] - 符合，已加入\n\n',
        'log.not_matched': '不符合，下一张\n\n',
        'log.processing': '处理中...\n\n',
        'log.done': '处理完成！',
        'folder.matched': '符合的图片',
        'folder.horizontal': '横图',
        'folder.vertical': '竖图',
        'folder.square': '方图',
        'folder.intersection': '交集',
        'folder.left_diff': '左差集',
        'folder.right_diff': '右差集',
        'folder.symmetric_diff': '对称差集',
    },
    'en': {
        'nav.duplicate': 'Duplicates',
        'nav.ratio': 'Aspect Ratio',
        'nav.size': 'Dimensions',
        'nav.classify': 'Classify',
        'nav.collection': 'Set Compare',
        'nav.about': 'About',
        'app.version': 'Version {version}',
        'sidebar.language': 'Language',
        'sidebar.appearance': 'Appearance',
        'theme.system': 'System',
        'theme.light': 'Light',
        'theme.dark': 'Dark',
        'button.browse': 'Browse',
        'button.start': 'Start',
        'status.ready': 'Ready',
        'label.input_dir': 'Input folder',
        'label.output_dir': 'Output folder',
        'label.left_input_dir': 'Left input folder',
        'label.right_input_dir': 'Right input folder',
        'label.image_type': 'Image type',
        'label.min_ratio': 'Min ratio',
        'label.max_ratio': 'Max ratio',
        'label.min_width': 'Min width',
        'label.max_width': 'Max width',
        'label.min_height': 'Min height',
        'label.max_height': 'Max height',
        'image_type.all': 'All',
        'image_type.horizontal': 'Landscape',
        'image_type.vertical': 'Portrait',
        'image_type.square': 'Square',
        'tip.prefix': 'Tip',
        'tip.duplicate': 'Duplicate detection deletes redundant images immediately. Back up important files before running.',
        'tip.ratio': 'Filter images by aspect ratio. Matches are copied to the output folder.',
        'tip.size': 'Filter images by pixel dimensions. Matches are copied to the output folder.',
        'tip.classify': 'Sort images into landscape, portrait, and square folders.',
        'tip.collection': 'Compare two image sets with intersection and difference operations. Results are copied to the output folder.',
        'collection.intersection': 'Intersection',
        'collection.left_diff': 'Left only',
        'collection.right_diff': 'Right only',
        'collection.symmetric_diff': 'Symmetric difference',
        'about.description': 'A batch image filtering tool built on Pillow for organizing large image collections.',
        'about.feature.duplicate': 'Duplicate detection',
        'about.feature.ratio': 'Aspect ratio filtering',
        'about.feature.size': 'Pixel dimension filtering',
        'about.feature.classify': 'Landscape / portrait / square classification',
        'about.feature.collection': 'Set comparison between two image groups',
        'about.project': 'Project',
        'about.checking': 'Checking for updates…',
        'about.up_to_date': 'You are up to date',
        'about.update_available': 'Version {version} is available',
        'about.check_failed': 'Update check failed. Please try again later.',
        'error.title.input': 'Invalid input',
        'error.title.selection': 'Invalid selection',
        'error.path_missing': 'The folder does not exist. Please choose again.',
        'error.same_in_out': 'Input and output folders must be different. Please choose again.',
        'error.left_same_out': 'The left input folder and the output folder must be different. Please choose again.',
        'error.right_same_out': 'The right input folder and the output folder must be different. Please choose again.',
        'error.left_same_right': 'The left and right input folders must be different. Please choose again.',
        'error.ratio_empty': 'Aspect ratio values cannot be empty.',
        'error.ratio_order': 'The maximum ratio cannot be smaller than the minimum ratio.',
        'error.value_empty': 'Values cannot be empty.',
        'error.limit_order': 'Maximum values cannot be smaller than minimum values.',
        'error.too_large': 'Values are too large.',
        'error.positive_integer': 'Values must be positive integers.',
        'error.select_type': 'Select at least one image type.',
        'error.select_set': 'Select at least one set operation.',
        'validation.positive_integer': 'Enter a positive integer.',
        'validation.number': 'Enter a valid number.',
        'log.duplicate_deleted': '[ {name} ] - duplicate, deleted\n\n',
        'log.no_duplicate': 'No duplicate, next image\n\n',
        'log.matched': '[ {name} ] - matched, copied\n\n',
        'log.not_matched': 'Not matched, next image\n\n',
        'log.processing': 'Processing...\n\n',
        'log.done': 'Done!',
        'folder.matched': 'Matched',
        'folder.horizontal': 'Landscape',
        'folder.vertical': 'Portrait',
        'folder.square': 'Square',
        'folder.intersection': 'Intersection',
        'folder.left_diff': 'Left only',
        'folder.right_diff': 'Right only',
        'folder.symmetric_diff': 'Symmetric difference',
    },
}

TYPE_FOLDER_KEYS = {
    0: 'folder.square',
    1: 'folder.horizontal',
    2: 'folder.vertical',
}

_current = DEFAULT_LANGUAGE


def _settings_path():
    base = os.environ.get('APPDATA') or tempfile.gettempdir()
    return os.path.join(base, 'PicFilter', 'settings.json')


def load_language():
    global _current
    try:
        with open(_settings_path(), encoding='utf-8') as settings:
            language = json.load(settings).get('language')
    except (OSError, ValueError, AttributeError):
        language = None
    if language in TRANSLATIONS:
        _current = language
    return _current


def save_language(language):
    path = _settings_path()
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        settings = {}
        try:
            with open(path, encoding='utf-8') as current:
                settings = json.load(current)
            if not isinstance(settings, dict):
                settings = {}
        except (OSError, ValueError):
            settings = {}
        settings['language'] = language
        with open(path, 'w', encoding='utf-8') as target:
            json.dump(settings, target, ensure_ascii=False, indent=2)
    except OSError:
        pass


def set_language(language):
    global _current
    if language in TRANSLATIONS:
        _current = language


def get_language():
    return _current


def tr(key, **values):
    table = TRANSLATIONS.get(_current, TRANSLATIONS[DEFAULT_LANGUAGE])
    text = table.get(key) or TRANSLATIONS[DEFAULT_LANGUAGE].get(key) or key
    if not values:
        return text
    try:
        return text.format(**values)
    except (KeyError, IndexError):
        return text


def type_folder(index):
    return tr(TYPE_FOLDER_KEYS.get(index, 'folder.square'))
