import base64
import os
import tempfile
import tkinter as tk
import webbrowser
from tkinter import filedialog, messagebox

import customtkinter as ctk
from PIL import Image

from filter import Filter
from utils.Icon import Icon

FONT_FAMILY = 'Microsoft YaHei UI'
PROJECT_URL = 'https://github.com/Exisi/PicFilter'

IMAGE_TYPES = ('全部', '横图', '竖图')
IMAGE_TYPE_INDEX = {'全部': 0, '横图': 1, '竖图': 2}

THEME_MODES = {'跟随系统': 'system', '浅色': 'light', '深色': 'dark'}

NAV_ITEMS = ('图片去重', '比例限制', '宽高限制', '图片分类', '集合选区', '关于')

NAV_ICON_FILES = {
    '图片去重': 'clone',
    '比例限制': 'crop-simple',
    '宽高限制': 'maximize',
    '图片分类': 'table-cells-large',
    '集合选区': 'object-group',
    '关于': 'circle-info',
}

ICON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'icons')
ICON_SIZE = (18, 18)

SIDEBAR_WIDTH = 216


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.version = '0.2.2'
        self.icon_path = os.path.join(tempfile.gettempdir(), 'picfilter.ico')

        ctk.set_appearance_mode('system')
        ctk.set_default_color_theme('blue')

        self.title('PicFilter')
        self._apply_icon()
        self._init_fonts()

        self.inputname = tk.StringVar()
        self.outputname = tk.StringVar()
        self._inputname = tk.StringVar()

        self.w, self.h = 940, 720
        self._center_window()
        self.minsize(820, 640)
        self.resizable(True, True)

        self.messagebox = messagebox
        self.sidebar_visible = True
        self.pages = {}
        self.nav_buttons = {}
        self._icon_cache = {}
        self.current_page = None
        self._build_ui()
        self.show_page(NAV_ITEMS[0])
        self.update_idletasks()
        self.deiconify()

    # ---------------------------------------------------------------- window

    def _apply_icon(self):
        try:
            with open(self.icon_path, 'wb') as tmp:
                tmp.write(base64.b64decode(Icon().img))
            self.iconbitmap(self.icon_path)
        except OSError:
            pass

    def _init_fonts(self):
        self.font_title = ctk.CTkFont(family=FONT_FAMILY, size=22, weight='bold')
        self.font_page = ctk.CTkFont(family=FONT_FAMILY, size=18, weight='bold')
        self.font_subtitle = ctk.CTkFont(family=FONT_FAMILY, size=12)
        self.font_body = ctk.CTkFont(family=FONT_FAMILY, size=13)
        self.font_button = ctk.CTkFont(family=FONT_FAMILY, size=14, weight='bold')
        self.font_log = ctk.CTkFont(family=FONT_FAMILY, size=13)

    def _center_window(self):
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = int((screen_w - self.w) / 2)
        y = int((screen_h - self.h) / 2)
        self.geometry('{}x{}+{}+{}'.format(self.w, self.h, x, y))

    def _change_theme(self, value):
        ctk.set_appearance_mode(THEME_MODES.get(value, 'system'))

    def _create_icon(self, name, active=False):
        key = (name, active)
        if key not in self._icon_cache:
            suffix = '-active' if active else ''
            light = Image.open(
                os.path.join(ICON_DIR, '{}{}-light.png'.format(name, suffix))
            )
            dark = Image.open(
                os.path.join(ICON_DIR, '{}{}-dark.png'.format(name, suffix))
            )
            self._icon_cache[key] = ctk.CTkImage(
                light_image=light, dark_image=dark, size=ICON_SIZE
            )
        return self._icon_cache[key]

    # ---------------------------------------------------------------- layout

    def _build_ui(self):
        self.body = ctk.CTkFrame(self, fg_color='transparent')
        self.body.pack(fill='both', expand=True)
        self.body.grid_columnconfigure(1, weight=1)
        self.body.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_content()

    def _build_sidebar(self):
        self.sidebar_slot = ctk.CTkFrame(
            self.body,
            width=SIDEBAR_WIDTH,
            corner_radius=0,
            fg_color='transparent',
        )
        self.sidebar_slot.grid(row=0, column=0, sticky='nsw')
        self.sidebar_slot.grid_propagate(False)

        self.sidebar = ctk.CTkFrame(
            self.sidebar_slot,
            width=SIDEBAR_WIDTH,
            corner_radius=0,
            fg_color=('gray94', 'gray17'),
        )
        self.sidebar.place(x=0, y=0, relheight=1.0)
        self.sidebar.place_configure(
            width=self.sidebar._apply_widget_scaling(SIDEBAR_WIDTH)
        )
        self.sidebar.grid_columnconfigure(0, weight=1)
        self.sidebar.grid_rowconfigure(2, weight=1)

        brand = ctk.CTkFrame(self.sidebar, fg_color='transparent')
        brand.grid(row=0, column=0, sticky='ew', padx=18, pady=(24, 20))
        ctk.CTkLabel(
            brand, text='PicFilter', font=self.font_title, anchor='w'
        ).pack(anchor='w')
        ctk.CTkLabel(
            brand,
            text='版本 ' + self.version,
            font=self.font_subtitle,
            text_color=('gray45', 'gray60'),
            anchor='w',
        ).pack(anchor='w')

        nav = ctk.CTkFrame(self.sidebar, fg_color='transparent')
        nav.grid(row=1, column=0, sticky='ew', padx=10)
        nav.grid_columnconfigure(0, weight=1)
        for index, name in enumerate(NAV_ITEMS):
            button = ctk.CTkButton(
                nav,
                text='   ' + name,
                image=self._create_icon(NAV_ICON_FILES[name]),
                compound='left',
                anchor='w',
                height=38,
                corner_radius=8,
                fg_color='transparent',
                hover_color=('gray85', 'gray26'),
                text_color=('gray10', 'gray90'),
                font=self.font_body,
                command=lambda page=name: self.show_page(page),
            )
            button.grid(row=index, column=0, sticky='ew', padx=4, pady=2)
            self.nav_buttons[name] = button

        footer = ctk.CTkFrame(self.sidebar, fg_color='transparent')
        footer.grid(row=3, column=0, sticky='ew', padx=14, pady=(10, 18))
        ctk.CTkLabel(
            footer,
            text='外观',
            font=self.font_subtitle,
            text_color=('gray45', 'gray60'),
            anchor='w',
        ).pack(anchor='w', pady=(0, 6))
        theme_switch = ctk.CTkSegmentedButton(
            footer,
            values=list(THEME_MODES.keys()),
            width=SIDEBAR_WIDTH - 28,
            height=30,
            font=self.font_subtitle,
            command=self._change_theme,
        )
        theme_switch.set('跟随系统')
        theme_switch.pack(anchor='w')

    def toggle_sidebar(self):
        page = self.pages.get(self.current_page)
        if page is not None:
            page.grid_remove()

        self.sidebar_visible = not self.sidebar_visible
        self.sidebar_slot.configure(
            width=SIDEBAR_WIDTH if self.sidebar_visible else 0
        )
        self.menu_button.configure(
            image=self._create_icon(
                'chevron-left' if self.sidebar_visible else 'bars'
            )
        )

        if page is not None:
            page.grid()

    def _build_content(self):
        self.content = ctk.CTkFrame(self.body, fg_color='transparent')
        self.content.grid(row=0, column=1, sticky='nsew', padx=16, pady=(12, 16))
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(1, weight=1)

        topbar = ctk.CTkFrame(self.content, fg_color='transparent')
        topbar.grid(row=0, column=0, sticky='ew')
        topbar.grid_columnconfigure(1, weight=1)

        self.menu_button = ctk.CTkButton(
            topbar,
            text='',
            image=self._create_icon('chevron-left'),
            width=38,
            height=32,
            corner_radius=8,
            fg_color=('gray85', 'gray25'),
            hover_color=('gray78', 'gray32'),
            command=self.toggle_sidebar,
        )
        self.menu_button.grid(row=0, column=0, sticky='w')

        self.page_title = ctk.CTkLabel(
            topbar, text='', font=self.font_page, anchor='w'
        )
        self.page_title.grid(row=0, column=1, sticky='w', padx=14)

        self.page_area = ctk.CTkFrame(self.content, fg_color='transparent')
        self.page_area.grid(row=1, column=0, sticky='nsew', pady=(10, 0))
        self.page_area.grid_columnconfigure(0, weight=1)
        self.page_area.grid_rowconfigure(0, weight=1)

        builders = {
            '图片去重': self.duplicate_tab,
            '比例限制': self.ratio_tab,
            '宽高限制': self.size_tab,
            '图片分类': self.classify_tab,
            '集合选区': self.collection_tab,
            '关于': self.about_tab,
        }
        for name in NAV_ITEMS:
            page = ctk.CTkFrame(
                self.page_area,
                corner_radius=14,
                fg_color=('gray92', 'gray15'),
            )
            page.grid_columnconfigure(0, weight=1)
            builders[name](page)
            self.pages[name] = page

        for name in NAV_ITEMS:
            self.pages[name].grid(row=0, column=0, sticky='nsew')
        self.update_idletasks()
        for name in NAV_ITEMS:
            self.pages[name].grid_remove()

    def show_page(self, name):
        if name == self.current_page:
            return

        previous = self.current_page
        self.pages[name].grid(row=0, column=0, sticky='nsew')
        if previous is not None:
            self.pages[previous].grid_remove()

        self.current_page = name
        self.page_title.configure(text=name)

        for page_name in (previous, name):
            if page_name is None:
                continue
            selected = page_name == name
            self.nav_buttons[page_name].configure(
                fg_color=('gray78', 'gray30') if selected else 'transparent',
                image=self._create_icon(NAV_ICON_FILES[page_name], active=selected),
            )

    def _create_card(self, tab):
        tab.grid_columnconfigure(0, weight=1)
        return tab

    def _add_tip(self, card, text):
        ctk.CTkLabel(
            card,
            text='提示  ' + text,
            font=self.font_body,
            text_color=('gray35', 'gray72'),
            anchor='w',
            justify='left',
            wraplength=560,
        ).grid(row=0, column=0, sticky='ew', padx=16, pady=(14, 2))

    def _add_path_row(self, card, row, label, variable, browse_command):
        line = ctk.CTkFrame(card, fg_color='transparent')
        line.grid(row=row, column=0, sticky='ew', padx=16, pady=(10, 0))
        line.columnconfigure(1, weight=1)

        ctk.CTkLabel(
            line, text=label, width=76, anchor='w', font=self.font_body
        ).grid(row=0, column=0, padx=(0, 8))
        entry = ctk.CTkEntry(
            line, textvariable=variable, height=34, font=self.font_body
        )
        entry.grid(row=0, column=1, sticky='ew')
        ctk.CTkButton(
            line,
            text='浏览',
            width=64,
            height=34,
            font=self.font_body,
            command=browse_command,
        ).grid(row=0, column=2, padx=(8, 0))
        return entry

    def _add_option_group(self, card, row, pady=(12, 0)):
        group = ctk.CTkFrame(card, corner_radius=10, fg_color=('gray90', 'gray20'))
        group.grid(row=row, column=0, sticky='ew', padx=16, pady=pady)
        return group

    def _add_option_label(self, parent, text, row=0, column=0, padx=(0, 8)):
        label = ctk.CTkLabel(parent, text=text, font=self.font_body, anchor='w')
        label.grid(row=row, column=column, sticky='w', padx=padx, pady=10)
        return label

    def _create_number_entry(self, parent, width=96, default='', is_float=False):
        validator = self._ratio_value_validate if is_float else self._wh_value_validate
        command = self.register(validator)
        entry = ctk.CTkEntry(
            parent,
            width=width,
            height=34,
            font=self.font_body,
            justify='center',
            validate='focusout',
            validatecommand=(command, '%P'),
        )
        if default:
            entry.insert(0, default)
        return entry

    def _add_log(self, card, row, height=230):
        box = ctk.CTkTextbox(
            card,
            height=height,
            wrap='char',
            state='disabled',
            corner_radius=10,
            border_width=1,
            font=self.font_log,
        )
        box.grid(row=row, column=0, sticky='nsew', padx=16, pady=(12, 0))
        card.rowconfigure(row, weight=1)
        return box

    def _add_action_bar(self, card, row, command):
        bar = ctk.CTkFrame(card, fg_color='transparent')
        bar.grid(row=row, column=0, sticky='ew', padx=16, pady=12)
        bar.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            bar,
            text='就绪',
            font=self.font_subtitle,
            text_color=('gray45', 'gray60'),
            anchor='w',
        ).grid(row=0, column=0, sticky='w')

        button = ctk.CTkButton(
            bar,
            text='开始处理',
            width=136,
            height=38,
            corner_radius=10,
            font=self.font_button,
            command=command,
        )
        button.grid(row=0, column=1, sticky='e')
        return button

    # ------------------------------------------------------------------ tabs

    def duplicate_tab(self, tab):
        card = self._create_card(tab)
        self._add_tip(card, '图片去重会直接删除重复的图片，操作前请先备份重要文件。')
        self._add_path_row(
            card, 1, '输入目录', self.inputname, self.get_input_dir
        ).focus()
        mes = self._add_log(card, 2)
        start_btn = self._add_action_bar(
            card, 3, lambda: Filter.duplicate_start(self, mes, start_btn)
        )

    def ratio_tab(self, tab):
        card = self._create_card(tab)
        self._add_tip(card, '按图片长宽比例筛选，符合的图片会复制到输出目录。')
        self._add_path_row(card, 1, '输入目录', self.inputname, self.get_input_dir)
        self._add_path_row(card, 2, '输出目录', self.outputname, self.get_output_dir)

        group = self._add_option_group(card, 3)
        self._add_option_label(group, '图片类型')
        image_type = ctk.CTkOptionMenu(
            group,
            values=list(IMAGE_TYPES),
            width=110,
            height=34,
            font=self.font_body,
        )
        image_type.set(IMAGE_TYPES[0])
        image_type.grid(row=0, column=1, padx=(0, 24), pady=10)

        self._add_option_label(group, '最小比例', column=2)
        min_scale = self._create_number_entry(group, default='1.0', is_float=True)
        min_scale.grid(row=0, column=3, padx=(0, 24), pady=10)

        self._add_option_label(group, '最大比例', column=4)
        max_scale = self._create_number_entry(group, default='1.0', is_float=True)
        max_scale.grid(row=0, column=5, padx=(0, 12), pady=10)

        mes = self._add_log(card, 4)
        start_btn = self._add_action_bar(
            card,
            5,
            lambda: Filter.scale_start(
                self,
                mes,
                start_btn,
                IMAGE_TYPE_INDEX[image_type.get()],
                max_scale,
                min_scale,
            ),
        )

    def size_tab(self, tab):
        card = self._create_card(tab)
        self._add_tip(card, '按图片宽高像素范围筛选，符合的图片会复制到输出目录。')
        self._add_path_row(card, 1, '输入目录', self.inputname, self.get_input_dir)
        self._add_path_row(card, 2, '输出目录', self.outputname, self.get_output_dir)

        group = self._add_option_group(card, 3)
        self._add_option_label(group, '最小宽度')
        min_width = self._create_number_entry(group)
        min_width.grid(row=0, column=1, padx=(0, 24), pady=10)
        self._add_option_label(group, '最大宽度', column=2)
        max_width = self._create_number_entry(group)
        max_width.grid(row=0, column=3, padx=(0, 12), pady=10)

        self._add_option_label(group, '最小高度', row=1)
        min_height = self._create_number_entry(group)
        min_height.grid(row=1, column=1, padx=(0, 24), pady=(0, 10))
        self._add_option_label(group, '最大高度', row=1, column=2)
        max_height = self._create_number_entry(group)
        max_height.grid(row=1, column=3, padx=(0, 12), pady=(0, 10))

        limit = {
            'maxH': max_height,
            'minH': min_height,
            'maxW': max_width,
            'minW': min_width,
        }
        mes = self._add_log(card, 4)
        start_btn = self._add_action_bar(
            card, 5, lambda: Filter.limit_start(self, mes, start_btn, limit)
        )

    def classify_tab(self, tab):
        card = self._create_card(tab)
        self._add_tip(card, '按横图 / 竖图 / 方图对图片进行分类。')
        self._add_path_row(card, 1, '输入目录', self.inputname, self.get_input_dir)
        self._add_path_row(card, 2, '输出目录', self.outputname, self.get_output_dir)

        group = self._add_option_group(card, 3)
        horizontal = tk.IntVar(value=1)
        vertical = tk.IntVar(value=1)
        square = tk.IntVar(value=1)
        checkboxes = (
            ('横图', horizontal),
            ('竖图', vertical),
            ('方图', square),
        )
        for index, (text, variable) in enumerate(checkboxes):
            ctk.CTkCheckBox(
                group,
                text=text,
                variable=variable,
                font=self.font_body,
                checkbox_width=22,
                checkbox_height=22,
            ).grid(row=0, column=index, sticky='w', padx=(16 if index == 0 else 20, 0), pady=12)
        check = [horizontal, vertical, square]

        mes = self._add_log(card, 4)
        start_btn = self._add_action_bar(
            card, 5, lambda: Filter.classify_start(self, mes, start_btn, check)
        )

    def collection_tab(self, tab):
        card = self._create_card(tab)
        self._add_tip(card, '对两组图片做交集 / 差集，结果会复制到输出目录。')
        self._add_path_row(card, 1, '左输入目录', self.inputname, self.get_input_dir)
        self._add_path_row(card, 2, '右输入目录', self._inputname, self.get__input_dir)
        self._add_path_row(card, 3, '输出目录', self.outputname, self.get_output_dir)

        group = self._add_option_group(card, 4)
        intersection = tk.IntVar()
        left_diff = tk.IntVar()
        right_diff = tk.IntVar()
        symmetry_diff = tk.IntVar()
        checkboxes = (
            ('交集', intersection),
            ('左差集', left_diff),
            ('右差集', right_diff),
            ('对称差集', symmetry_diff),
        )
        for index, (text, variable) in enumerate(checkboxes):
            ctk.CTkCheckBox(
                group,
                text=text,
                variable=variable,
                font=self.font_body,
                checkbox_width=22,
                checkbox_height=22,
            ).grid(row=0, column=index, sticky='w', padx=(16 if index == 0 else 18, 0), pady=12)
        check = [intersection, left_diff, right_diff, symmetry_diff]

        mes = self._add_log(card, 5)
        start_btn = self._add_action_bar(
            card, 6, lambda: Filter.collection_start(self, mes, start_btn, check)
        )

    def about_tab(self, tab):
        card = self._create_card(tab)
        content = ctk.CTkFrame(card, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=28, pady=26)

        ctk.CTkLabel(
            content,
            text='PicFilter',
            font=ctk.CTkFont(family=FONT_FAMILY, size=30, weight='bold'),
            anchor='w',
        ).pack(fill='x')
        ctk.CTkLabel(
            content,
            text='版本 ' + self.version,
            font=self.font_subtitle,
            text_color=('gray40', 'gray65'),
            anchor='w',
        ).pack(fill='x', pady=(2, 18))
        ctk.CTkLabel(
            content,
            text='一个基于 Pillow 的批量图片筛选工具，适用于整理大量图片。',
            font=self.font_body,
            anchor='w',
            justify='left',
            wraplength=560,
        ).pack(fill='x')

        features = (
            '图片去重',
            '长宽比例筛选',
            '宽高像素筛选',
            '横 / 竖 / 方图分类',
            '两组图片的集合对比',
        )
        for feature in features:
            ctk.CTkLabel(
                content,
                text='·  ' + feature,
                font=self.font_body,
                text_color=('gray30', 'gray75'),
                anchor='w',
            ).pack(fill='x', pady=(8, 0))

        ctk.CTkLabel(
            content,
            text='项目地址',
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight='bold'),
            anchor='w',
        ).pack(fill='x', pady=(22, 4))
        ctk.CTkButton(
            content,
            text=PROJECT_URL,
            anchor='w',
            width=400,
            height=32,
            fg_color='transparent',
            hover_color=('gray85', 'gray28'),
            text_color=('#1f6feb', '#58a6ff'),
            font=self.font_body,
            command=lambda: webbrowser.open(PROJECT_URL),
        ).pack(anchor='w')

    # -------------------------------------------------------------- handlers

    def _wh_value_validate(self, value):
        if value == '' or value.isdigit():
            return True
        messagebox.showinfo(title='输入错误', message='请输入正整数数字！')
        return False

    def _ratio_value_validate(self, value):
        if value == '':
            return True
        try:
            float(value)
            return True
        except ValueError:
            messagebox.showinfo(title='输入错误', message='请输入有效数字！')
            return False

    def get_input_dir(self):
        self.inputname.set(filedialog.askdirectory())

    def get__input_dir(self):
        self._inputname.set(filedialog.askdirectory())

    def get_output_dir(self):
        self.outputname.set(filedialog.askdirectory())


if __name__ == '__main__':
    app = App()
    app.mainloop()
    try:
        os.remove(app.icon_path)
    except OSError:
        pass
