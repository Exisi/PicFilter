import base64
import json
import os
import queue
import re
import sys
import tempfile
import threading
import tkinter as tk
import urllib.request
import webbrowser
from tkinter import filedialog, messagebox

import customtkinter as ctk
from PIL import Image

from filter import Filter
from utils import I18n, Settings
from utils.Icon import Icon

FONT_FAMILY = 'Microsoft YaHei UI'
PROJECT_URL = 'https://github.com/Exisi/PicFilter'
UPDATE_API_URL = 'https://api.github.com/repos/Exisi/PicFilter/releases/latest'

IMAGE_TYPE_KEYS = ('all', 'horizontal', 'vertical')

NAV_PAGES = ('duplicate', 'ratio', 'size', 'classify', 'collection', 'about')

NAV_ICON_FILES = {
    'duplicate': 'clone',
    'ratio': 'crop-simple',
    'size': 'maximize',
    'classify': 'table-cells-large',
    'collection': 'object-group',
    'about': 'circle-info',
}

def _resource_dir():
    return getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))


def _load_version(fallback='0.2.2'):
    try:
        path = os.path.join(_resource_dir(), 'package.json')
        with open(path, encoding='utf-8') as manifest:
            return json.load(manifest).get('version', fallback)
    except (OSError, ValueError):
        return fallback


ICON_DIR = os.path.join(_resource_dir(), 'assets', 'icons')
ICON_SIZE = (18, 18)

SIDEBAR_WIDTH = 216

ACCENT = ('#2563eb', '#3b82f6')
ACCENT_HOVER = ('#1d4ed8', '#60a5fa')
NAV_TEXT = ('#1f2328', '#e8eaed')
NAV_SELECTED_BG = ('#dce9fe', '#243752')
NAV_SELECTED_TEXT = ('#1d4ed8', '#93c5fd')
NAV_HOVER_BG = ('#e9f1fe', '#2d3f58')
SEGMENTED_UNSELECTED = ('gray90', 'gray22')
SEGMENTED_UNSELECTED_HOVER = ('gray84', 'gray28')


def _image_type_labels():
    return [I18n.tr('image_type.' + key) for key in IMAGE_TYPE_KEYS]


def _parse_version(text):
    match = re.search(r'\d+(?:\.\d+)*', text or '')
    if match is None:
        return ()
    parts = [int(part) for part in match.group(0).split('.')]
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        I18n.load_language()
        self.version = _load_version()
        saved_theme = Settings.load().get('appearance')
        self.theme_key = saved_theme if saved_theme in ('light', 'dark') else 'system'
        self.icon_path = os.path.join(tempfile.gettempdir(), 'picfilter.ico')

        ctk.set_appearance_mode(self.theme_key)
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
        self._ui_generation = 0
        self._update_url = PROJECT_URL
        self._update_checking = False
        self._update_frames = None
        self.current_page = None
        self._build_ui()
        self.show_page(NAV_PAGES[0])
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

    def _theme_icon(self):
        mode = 'moon' if ctk.get_appearance_mode() == 'Dark' else 'sun'
        return self._create_icon(mode, size=(20, 20))

    def _toggle_theme(self):
        self.theme_key = 'light' if ctk.get_appearance_mode() == 'Dark' else 'dark'
        ctk.set_appearance_mode(self.theme_key)
        Settings.save('appearance', self.theme_key)
        self.theme_button.configure(image=self._theme_icon())

    def _select_language(self, label):
        language = next(
            (code for code, text in I18n.LANGUAGE_LABELS.items() if text == label),
            None,
        )
        if language is None or language == I18n.get_language():
            return
        I18n.set_language(language)
        I18n.save_language(language)
        self._rebuild_ui()

    def _rebuild_ui(self):
        page = self.current_page or NAV_PAGES[0]
        self._ui_generation += 1
        self._update_checking = False
        self.body.destroy()
        self.pages.clear()
        self.nav_buttons.clear()
        self.current_page = None
        self._build_ui()
        if not self.sidebar_visible:
            self.sidebar_slot.configure(width=0)
            self.menu_button.configure(image=self._create_icon('bars'))
        self.show_page(page)

    def _create_icon(self, name, active=False, size=ICON_SIZE):
        key = (name, active, size)
        if key not in self._icon_cache:
            suffix = '-active' if active else ''
            light = Image.open(
                os.path.join(ICON_DIR, '{}{}-light.png'.format(name, suffix))
            )
            dark = Image.open(
                os.path.join(ICON_DIR, '{}{}-dark.png'.format(name, suffix))
            )
            self._icon_cache[key] = ctk.CTkImage(
                light_image=light, dark_image=dark, size=size
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
            text=I18n.tr('app.version', version=self.version),
            font=self.font_subtitle,
            text_color=('gray45', 'gray60'),
            anchor='w',
        ).pack(anchor='w')

        nav = ctk.CTkFrame(self.sidebar, fg_color='transparent')
        nav.grid(row=1, column=0, sticky='ew', padx=10)
        nav.grid_columnconfigure(0, weight=1)
        for index, name in enumerate(NAV_PAGES):
            button = ctk.CTkButton(
                nav,
                text='   ' + I18n.tr('nav.' + name),
                image=self._create_icon(NAV_ICON_FILES[name]),
                compound='left',
                anchor='w',
                height=38,
                corner_radius=8,
                fg_color='transparent',
                hover_color=NAV_HOVER_BG,
                text_color=NAV_TEXT,
                font=self.font_body,
                command=lambda page=name: self.show_page(page),
            )
            button.grid(row=index, column=0, sticky='ew', padx=4, pady=2)
            self.nav_buttons[name] = button

        footer = ctk.CTkFrame(self.sidebar, fg_color='transparent')
        footer.grid(row=3, column=0, sticky='ew', padx=14, pady=(10, 18))
        footer.grid_columnconfigure(0, weight=1)

        language_row = ctk.CTkFrame(footer, fg_color='transparent')
        language_row.grid(row=0, column=0, sticky='ew')
        ctk.CTkLabel(
            language_row,
            text=I18n.tr('sidebar.language'),
            font=self.font_subtitle,
            text_color=('gray45', 'gray60'),
            anchor='w',
        ).pack(side='left')
        self.language_menu = ctk.CTkOptionMenu(
            language_row,
            width=104,
            height=32,
            corner_radius=8,
            values=list(I18n.LANGUAGE_LABELS.values()),
            command=self._select_language,
            fg_color=SEGMENTED_UNSELECTED,
            button_color=SEGMENTED_UNSELECTED,
            button_hover_color=SEGMENTED_UNSELECTED_HOVER,
            text_color=NAV_TEXT,
            font=self.font_subtitle,
            dropdown_fg_color=SEGMENTED_UNSELECTED,
            dropdown_hover_color=NAV_HOVER_BG,
            dropdown_text_color=NAV_TEXT,
            dropdown_font=self.font_subtitle,
        )
        self.language_menu.set(I18n.LANGUAGE_LABELS[I18n.get_language()])
        self.language_menu.pack(side='right')

        theme_row = ctk.CTkFrame(footer, fg_color='transparent')
        theme_row.grid(row=1, column=0, sticky='ew', pady=(8, 0))
        ctk.CTkLabel(
            theme_row,
            text=I18n.tr('sidebar.appearance'),
            font=self.font_subtitle,
            text_color=('gray45', 'gray60'),
            anchor='w',
        ).pack(side='left')
        self.theme_button = ctk.CTkButton(
            theme_row,
            width=32,
            height=32,
            corner_radius=8,
            text='',
            image=self._theme_icon(),
            fg_color='transparent',
            hover_color=NAV_HOVER_BG,
            command=self._toggle_theme,
        )
        self.theme_button.pack(side='right')

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
            width=32,
            height=32,
            corner_radius=8,
            fg_color='transparent',
            hover_color=NAV_HOVER_BG,
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
            'duplicate': self.duplicate_tab,
            'ratio': self.ratio_tab,
            'size': self.size_tab,
            'classify': self.classify_tab,
            'collection': self.collection_tab,
            'about': self.about_tab,
        }
        for name in NAV_PAGES:
            page = ctk.CTkFrame(
                self.page_area,
                corner_radius=14,
                fg_color=('gray92', 'gray15'),
            )
            page.grid_columnconfigure(0, weight=1)
            builders[name](page)
            self.pages[name] = page

        for name in NAV_PAGES:
            self.pages[name].grid(row=0, column=0, sticky='nsew')
        self.update_idletasks()
        for name in NAV_PAGES:
            self.pages[name].grid_remove()

    def show_page(self, name):
        if name == self.current_page:
            return

        previous = self.current_page
        self.pages[name].grid(row=0, column=0, sticky='nsew')
        if previous is not None:
            self.pages[previous].grid_remove()

        self.current_page = name
        self.page_title.configure(text=I18n.tr('nav.' + name))

        for page_name in (previous, name):
            if page_name is None:
                continue
            selected = page_name == name
            self.nav_buttons[page_name].configure(
                fg_color=NAV_SELECTED_BG if selected else 'transparent',
                text_color=NAV_SELECTED_TEXT if selected else NAV_TEXT,
                image=self._create_icon(NAV_ICON_FILES[page_name], active=selected),
            )

    def _create_card(self, tab):
        tab.grid_columnconfigure(0, weight=1)
        return tab

    def _add_tip(self, card, text):
        ctk.CTkLabel(
            card,
            text=I18n.tr('tip.prefix') + '  ' + text,
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
            text=I18n.tr('button.browse'),
            width=64,
            height=34,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
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
            text=I18n.tr('status.ready'),
            font=self.font_subtitle,
            text_color=('gray45', 'gray60'),
            anchor='w',
        ).grid(row=0, column=0, sticky='w')

        button = ctk.CTkButton(
            bar,
            text=I18n.tr('button.start'),
            width=136,
            height=38,
            corner_radius=10,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            font=self.font_button,
            command=command,
        )
        button.grid(row=0, column=1, sticky='e')
        return button

    # ------------------------------------------------------------------ tabs

    def duplicate_tab(self, tab):
        card = self._create_card(tab)
        self._add_tip(card, I18n.tr('tip.duplicate'))
        self._add_path_row(
            card, 1, I18n.tr('label.input_dir'), self.inputname, self.get_input_dir
        ).focus()
        mes = self._add_log(card, 2)
        start_btn = self._add_action_bar(
            card, 3, lambda: Filter.duplicate_start(self, mes, start_btn)
        )

    def ratio_tab(self, tab):
        card = self._create_card(tab)
        self._add_tip(card, I18n.tr('tip.ratio'))
        self._add_path_row(
            card, 1, I18n.tr('label.input_dir'), self.inputname, self.get_input_dir
        )
        self._add_path_row(
            card, 2, I18n.tr('label.output_dir'), self.outputname, self.get_output_dir
        )

        group = self._add_option_group(card, 3)
        self._add_option_label(group, I18n.tr('label.image_type'))
        labels = _image_type_labels()
        image_type = ctk.CTkOptionMenu(
            group,
            values=labels,
            width=110,
            height=34,
            fg_color=SEGMENTED_UNSELECTED,
            button_color=ACCENT,
            button_hover_color=ACCENT_HOVER,
            dropdown_fg_color=SEGMENTED_UNSELECTED,
            dropdown_hover_color=NAV_HOVER_BG,
            font=self.font_body,
        )
        image_type.set(labels[0])
        image_type.grid(row=0, column=1, padx=(0, 24), pady=10)

        self._add_option_label(group, I18n.tr('label.min_ratio'), column=2)
        min_scale = self._create_number_entry(group, default='1.0', is_float=True)
        min_scale.grid(row=0, column=3, padx=(0, 24), pady=10)

        self._add_option_label(group, I18n.tr('label.max_ratio'), column=4)
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
                labels.index(image_type.get()),
                max_scale,
                min_scale,
            ),
        )

    def size_tab(self, tab):
        card = self._create_card(tab)
        self._add_tip(card, I18n.tr('tip.size'))
        self._add_path_row(
            card, 1, I18n.tr('label.input_dir'), self.inputname, self.get_input_dir
        )
        self._add_path_row(
            card, 2, I18n.tr('label.output_dir'), self.outputname, self.get_output_dir
        )

        group = self._add_option_group(card, 3)
        self._add_option_label(group, I18n.tr('label.min_width'))
        min_width = self._create_number_entry(group, default='0')
        min_width.grid(row=0, column=1, padx=(0, 24), pady=10)
        self._add_option_label(group, I18n.tr('label.max_width'), column=2)
        max_width = self._create_number_entry(group, default='0')
        max_width.grid(row=0, column=3, padx=(0, 12), pady=10)

        self._add_option_label(group, I18n.tr('label.min_height'), row=1)
        min_height = self._create_number_entry(group, default='0')
        min_height.grid(row=1, column=1, padx=(0, 24), pady=(0, 10))
        self._add_option_label(group, I18n.tr('label.max_height'), row=1, column=2)
        max_height = self._create_number_entry(group, default='0')
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
        self._add_tip(card, I18n.tr('tip.classify'))
        self._add_path_row(
            card, 1, I18n.tr('label.input_dir'), self.inputname, self.get_input_dir
        )
        self._add_path_row(
            card, 2, I18n.tr('label.output_dir'), self.outputname, self.get_output_dir
        )

        group = self._add_option_group(card, 3)
        horizontal = tk.IntVar(value=1)
        vertical = tk.IntVar(value=1)
        square = tk.IntVar(value=1)
        checkboxes = (
            (I18n.tr('image_type.horizontal'), horizontal),
            (I18n.tr('image_type.vertical'), vertical),
            (I18n.tr('image_type.square'), square),
        )
        for index, (text, variable) in enumerate(checkboxes):
            ctk.CTkCheckBox(
                group,
                text=text,
                variable=variable,
                font=self.font_body,
                checkbox_width=22,
                checkbox_height=22,
                fg_color=ACCENT,
                hover_color=ACCENT_HOVER,
            ).grid(row=0, column=index, sticky='w', padx=(16 if index == 0 else 20, 0), pady=12)
        check = [horizontal, vertical, square]

        mes = self._add_log(card, 4)
        start_btn = self._add_action_bar(
            card, 5, lambda: Filter.classify_start(self, mes, start_btn, check)
        )

    def collection_tab(self, tab):
        card = self._create_card(tab)
        self._add_tip(card, I18n.tr('tip.collection'))
        self._add_path_row(
            card, 1, I18n.tr('label.left_input_dir'), self.inputname, self.get_input_dir
        )
        self._add_path_row(
            card, 2, I18n.tr('label.right_input_dir'), self._inputname, self.get__input_dir
        )
        self._add_path_row(
            card, 3, I18n.tr('label.output_dir'), self.outputname, self.get_output_dir
        )

        group = self._add_option_group(card, 4)
        intersection = tk.IntVar()
        left_diff = tk.IntVar()
        right_diff = tk.IntVar()
        symmetry_diff = tk.IntVar()
        checkboxes = (
            (I18n.tr('collection.intersection'), intersection),
            (I18n.tr('collection.left_diff'), left_diff),
            (I18n.tr('collection.right_diff'), right_diff),
            (I18n.tr('collection.symmetric_diff'), symmetry_diff),
        )
        for index, (text, variable) in enumerate(checkboxes):
            ctk.CTkCheckBox(
                group,
                text=text,
                variable=variable,
                font=self.font_body,
                checkbox_width=22,
                checkbox_height=22,
                fg_color=ACCENT,
                hover_color=ACCENT_HOVER,
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

        version_line = ctk.CTkFrame(content, fg_color='transparent')
        version_line.pack(fill='x', pady=(2, 18))
        ctk.CTkLabel(
            version_line,
            text=I18n.tr('app.version', version=self.version),
            font=self.font_subtitle,
            text_color=('gray40', 'gray65'),
            anchor='w',
        ).pack(side='left')
        self.update_action = ctk.CTkButton(
            version_line,
            text='',
            image=self._create_icon('arrows-rotate'),
            width=26,
            height=26,
            corner_radius=6,
            fg_color='transparent',
            hover_color=NAV_HOVER_BG,
            command=self._check_update,
        )
        self.update_action.pack(side='left', padx=(10, 0))
        self.update_status = ctk.CTkLabel(
            version_line,
            text='',
            font=self.font_subtitle,
            text_color=('gray45', 'gray60'),
            anchor='w',
        )
        self.update_status.pack(side='left', padx=(8, 0))

        ctk.CTkLabel(
            content,
            text=I18n.tr('about.description'),
            font=self.font_body,
            anchor='w',
            justify='left',
            wraplength=560,
        ).pack(fill='x')

        features = (
            I18n.tr('about.feature.duplicate'),
            I18n.tr('about.feature.ratio'),
            I18n.tr('about.feature.size'),
            I18n.tr('about.feature.classify'),
            I18n.tr('about.feature.collection'),
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
            text=I18n.tr('about.project'),
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
            hover_color=NAV_HOVER_BG,
            text_color=('#1f6feb', '#58a6ff'),
            font=self.font_body,
            command=lambda: webbrowser.open(PROJECT_URL),
        ).pack(anchor='w')

    def _check_update(self):
        if self._update_checking:
            return
        generation = self._ui_generation
        self._update_checking = True
        self.update_status.configure(text=I18n.tr('about.checking'))
        self._animate_update_icon(generation)
        results = queue.Queue()
        threading.Thread(
            target=self._check_update_worker,
            args=(results,),
            daemon=True,
        ).start()
        self.after(100, self._poll_update_result, generation, results)

    def _animate_update_icon(self, generation, index=0):
        if generation != self._ui_generation or not self._update_checking:
            return
        frames = self._spinner_frames()
        self.update_action.configure(image=frames[index % len(frames)])
        self.after(60, self._animate_update_icon, generation, index + 1)

    def _spinner_frames(self):
        if self._update_frames is None:
            light = Image.open(os.path.join(ICON_DIR, 'spinner-light.png'))
            dark = Image.open(os.path.join(ICON_DIR, 'spinner-dark.png'))
            self._update_frames = [
                ctk.CTkImage(
                    light_image=light.rotate(angle, resample=Image.BICUBIC),
                    dark_image=dark.rotate(angle, resample=Image.BICUBIC),
                    size=ICON_SIZE,
                )
                for angle in range(0, 360, 30)
            ]
        return self._update_frames

    def _check_update_worker(self, results):
        try:
            release = self._fetch_latest_release()
            tag = str(release.get('tag_name') or '')
            url = release.get('html_url') or PROJECT_URL
        except (OSError, ValueError, AttributeError):
            results.put((False, '', ''))
            return
        results.put((True, tag, url))

    def _poll_update_result(self, generation, results):
        if generation != self._ui_generation:
            return
        try:
            success, tag, url = results.get_nowait()
        except queue.Empty:
            self.after(100, self._poll_update_result, generation, results)
            return
        if success:
            self._handle_update_result(generation, tag, url)
        else:
            self._handle_update_error(generation)

    def _fetch_latest_release(self):
        request = urllib.request.Request(
            UPDATE_API_URL,
            headers={
                'Accept': 'application/vnd.github+json',
                'User-Agent': 'PicFilter/' + self.version,
            },
        )
        with urllib.request.urlopen(request, timeout=10) as response:
            release = json.loads(response.read().decode('utf-8'))
        if not isinstance(release, dict):
            raise ValueError('unexpected GitHub response')
        return release

    def _handle_update_result(self, generation, tag, url):
        if generation != self._ui_generation:
            return
        latest = _parse_version(tag)
        current = _parse_version(self.version)
        if not latest or not current:
            self._handle_update_error(generation)
            return
        if latest > current:
            self._update_url = url
            self._update_checking = False
            self.update_action.configure(
                image=self._create_icon('download'),
                command=self._open_update_url,
            )
            self.update_status.configure(
                text=I18n.tr('about.update_available', version=tag),
                text_color=('#1f6feb', '#58a6ff'),
            )
            return
        self.update_status.configure(
            text=I18n.tr('about.up_to_date'),
            text_color=('gray45', 'gray60'),
        )
        self._reset_update_action()

    def _handle_update_error(self, generation):
        if generation != self._ui_generation:
            return
        self.update_status.configure(
            text=I18n.tr('about.check_failed'),
            text_color=('gray45', 'gray60'),
        )
        self._reset_update_action()

    def _reset_update_action(self):
        self._update_checking = False
        self.update_action.configure(
            image=self._create_icon('arrows-rotate'),
            command=self._check_update,
        )

    def _open_update_url(self):
        webbrowser.open(self._update_url or PROJECT_URL)

    # -------------------------------------------------------------- handlers

    def _wh_value_validate(self, value):
        if value == '' or value.isdigit():
            return True
        messagebox.showinfo(
            title=I18n.tr('error.title.input'),
            message=I18n.tr('validation.positive_integer'),
        )
        return False

    def _ratio_value_validate(self, value):
        if value == '':
            return True
        try:
            float(value)
            return True
        except ValueError:
            messagebox.showinfo(
                title=I18n.tr('error.title.input'),
                message=I18n.tr('validation.number'),
            )
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
