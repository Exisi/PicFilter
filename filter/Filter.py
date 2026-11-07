import queue
import tkinter as tk
from threading import Thread

import filter.Load as Load
import filter.Image as Image
from utils import I18n

LOG_FLUSH_INTERVAL_MS = 80
LOG_FLUSH_BATCH = 200


def os_exist(in_dir, out_dir):
    '''
    Check whether the input and output paths exist
    :param in_dir: image input directory
    :param out_dir: image output path
    '''
    if out_dir is None:
        out_dir = in_dir
    if Load.exists(in_dir) and Load.exists(out_dir):
        return True
    else:
        return False


def is_duplicate_img(f, hist_dict):
    '''
    Detect duplicates using a dictionary keyed by the unique image pixel histogram
    :param f: image path
    :param hist_dict: histogram dictionary of already processed images
    '''
    hist = str(Image.hist(f))
    if hist not in hist_dict:
        hist_dict[hist] = f
        return False
    else:
        Load.delete(f)
        return True


def get_intersection(files, hist_dict):
    '''
    Return the intersection between image sets
    :param files: list of images
    :param hist_dict: histogram dictionary of the image list
    :return: dict
    '''
    inter_hist_dict = {}
    for f in files:
        hist = str(Image.hist(f))
        if (hist in hist_dict):
            inter_hist_dict[hist] = f
    return inter_hist_dict


def get_difference(hist_dict, inter_dict):
    '''
    Return the difference of a single set
    :param hist_dict: histogram dictionary of the left set
    :param inter_dict: intersection dictionary
    :return: list
    '''
    diff_dict = []
    for hist in hist_dict:
        if hist not in inter_dict:
            diff_dict.append(hist_dict[hist])
    return diff_dict


def _image_files(directory):
    '''
    Read the directory and keep only image files
    :param directory: image directory
    :return: list
    '''
    return [f for f in Load.read(directory) if Image.is_img(f)]


def _for_each(files, handler, report):
    '''
    Process images one by one; log a failure and continue with the remaining images
    :param files: list of images
    :param handler: handler for a single image
    :param report: log callback
    '''
    for f in files:
        try:
            handler(f)
        except Exception as exc:  # a single failed image must not abort the whole batch
            report(I18n.tr('log.file_failed', name=Load.name(f), error=exc))


def _widget_alive(widget):
    '''
    Check whether a Tk widget still exists (old widgets are destroyed when the UI is rebuilt)
    :param widget: Tk widget
    :return: bool
    '''
    try:
        return bool(widget.winfo_exists())
    except tk.TclError:
        return False


def _start_job(widget, log_box, button, work):
    '''
    Run an image-processing job on a background thread; all Tk widget access stays on the main thread.

    :param widget: Tk window (used for after scheduling)
    :param log_box: log text box
    :param button: start button
    :param work: processing function with signature work(report); report(str) writes to the log
    '''
    button.configure(state='disabled')
    log_box.configure(state='normal')
    log_box.delete('1.0', 'end')

    messages = queue.Queue()

    def report(text):
        messages.put(text)

    def worker():
        try:
            work(report)
        except Exception as exc:  # safety net: the button must be restored on any exception
            messages.put(I18n.tr('log.job_failed', error=exc))
        finally:
            messages.put(None)

    def poll():
        if not _widget_alive(log_box):
            return
        try:
            batch = []
            finished = False
            while len(batch) < LOG_FLUSH_BATCH:
                try:
                    item = messages.get_nowait()
                except queue.Empty:
                    break
                if item is None:
                    finished = True
                    break
                batch.append(item)
            if batch:
                log_box.insert('end', ''.join(batch))
                log_box.see('end')
            if finished:
                log_box.configure(state='disabled')
                button.configure(state='normal')
                return
            widget.after(LOG_FLUSH_INTERVAL_MS, poll)
        except tk.TclError:
            pass

    try:
        Thread(target=worker, daemon=True).start()
    except Exception as exc:
        messages.put(I18n.tr('log.job_failed', error=exc))
        messages.put(None)
    widget.after(LOG_FLUSH_INTERVAL_MS, poll)


def duplicate_start(self, mes, btn):
    '''
    Start the duplicate-removal job and validate the input
    :param self: GUI.App instance
    :param mes: GUI.fist_tab.scrolledtext progress messages
    :param btn: GUI.fist_tab.Button start button
    '''
    input_dir = self.inputname.get()
    if os_exist(input_dir, None):
        _start_job(self, mes, btn, lambda report: duplicate_removel(input_dir, report))
    else:
        self.messagebox.showinfo(title=I18n.tr('error.title.input'), message=I18n.tr('error.path_missing'))
        self.inputname.set('')


def scale_start(self, mes, btn, im_type, max_scale, min_scale):
    '''
    Start the aspect-ratio filter job and validate the input
    :param self: GUI.App instance
    :param mes: GUI.second_tab.scrolledtext progress messages
    :param btn: GUI.second_tab.Button start button
    :param im_type: image type (all/landscape/portrait)
    :param max_scale: maximum image aspect ratio
    :param min_scale: minimum image aspect ratio
    '''
    input_dir = self.inputname.get()
    output_dir = self.outputname.get()
    if not os_exist(input_dir, output_dir):
        self.messagebox.showinfo(title=I18n.tr('error.title.input'), message=I18n.tr('error.path_missing'))
        self.inputname.set('')
        self.outputname.set('')
        return
    if input_dir == output_dir:
        self.messagebox.showinfo(title=I18n.tr('error.title.input'), message=I18n.tr('error.same_in_out'))
        self.outputname.set('')
        return

    max_text = max_scale.get()
    min_text = min_scale.get()
    if max_text == '' or min_text == '':
        self.messagebox.showinfo(title=I18n.tr('error.title.input'), message=I18n.tr('error.ratio_empty'))
        return
    try:
        max_value = float(max_text)
        min_value = float(min_text)
    except ValueError:
        self.messagebox.showinfo(title=I18n.tr('error.title.input'), message=I18n.tr('validation.number'))
        return
    if max_value < min_value:
        self.messagebox.showinfo(title=I18n.tr('error.title.input'), message=I18n.tr('error.ratio_order'))
        return

    _start_job(
        self,
        mes,
        btn,
        lambda report: scale_selecter(input_dir, output_dir, im_type, max_value, min_value, report),
    )


def limit_start(self, mes, btn, limit):
    '''
    Start the width/height filter job and validate the input
    :param self: GUI.App instance
    :param mes: GUI.third_tab.scrolledtext progress messages
    :param btn: GUI.third_tab.Button start button
    :param limit: width and height limits dictionary (maxH,minH,maxW,minW)
    '''
    input_dir = self.inputname.get()
    output_dir = self.outputname.get()
    if not os_exist(input_dir, output_dir):
        self.messagebox.showinfo(title=I18n.tr('error.title.input'), message=I18n.tr('error.path_missing'))
        self.inputname.set('')
        self.outputname.set('')
        return
    if input_dir == output_dir:
        self.messagebox.showinfo(title=I18n.tr('error.title.input'), message=I18n.tr('error.same_in_out'))
        self.outputname.set('')
        return

    raw = {key: var.get() for key, var in limit.items()}
    if any(value == '' for value in raw.values()):
        self.messagebox.showinfo(title=I18n.tr('error.title.input'), message=I18n.tr('error.value_empty'))
        return
    if not all(value.isdigit() for value in raw.values()):
        self.messagebox.showinfo(title=I18n.tr('error.title.input'), message=I18n.tr('validation.positive_integer'))
        return

    values = {key: int(value) for key, value in raw.items()}
    if values['maxH'] < values['minH'] or values['maxW'] < values['minW']:
        self.messagebox.showinfo(title=I18n.tr('error.title.input'), message=I18n.tr('error.limit_order'))
        return
    if any(value > 99999 for value in values.values()):
        self.messagebox.showinfo(title=I18n.tr('error.title.input'), message=I18n.tr('error.too_large'))
        return

    _start_job(self, mes, btn, lambda report: limit_seleter(input_dir, output_dir, values, report))


def classify_start(self, mes, btn, check):
    '''
    Start the image classification job and validate the input
    :param self: GUI.App instance
    :param mes: GUI.fourth_tab.scrolledtext progress messages
    :param btn: GUI.fourth_tab.Button start button
    :param check: image types to include (square/landscape/portrait)
    '''
    input_dir = self.inputname.get()
    output_dir = self.outputname.get()
    if not os_exist(input_dir, output_dir):
        self.messagebox.showinfo(title=I18n.tr('error.title.input'), message=I18n.tr('error.path_missing'))
        self.inputname.set('')
        self.outputname.set('')
        return
    if input_dir == output_dir:
        self.messagebox.showinfo(title=I18n.tr('error.title.input'), message=I18n.tr('error.same_in_out'))
        self.outputname.set('')
        return

    checks = tuple(int(var.get()) for var in check)
    if all(value == 0 for value in checks):
        self.messagebox.showinfo(title=I18n.tr('error.title.selection'), message=I18n.tr('error.select_type'))
        return

    _start_job(self, mes, btn, lambda report: classify_selecter(input_dir, output_dir, checks, report))


def collection_start(self, mes, btn, check):
    '''
    Start the set-operation job and validate the input
    :param self: GUI.App instance
    :param mes: GUI.fourth_tab.scrolledtext progress messages
    :param btn: GUI.fourth_tab.Button start button
    :param check: set operation types (inter,l_diff,r_diff,lr_diff)
    '''
    left_dir = self.inputname.get()
    right_dir = self._inputname.get()
    output_dir = self.outputname.get()
    if not (os_exist(left_dir, output_dir) and os_exist(right_dir, None)):
        self.messagebox.showinfo(title=I18n.tr('error.title.input'), message=I18n.tr('error.path_missing'))
        self.inputname.set('')
        self._inputname.set('')
        self.outputname.set('')
        return
    if left_dir == output_dir:
        self.messagebox.showinfo(title=I18n.tr('error.title.input'), message=I18n.tr('error.left_same_out'))
        self.outputname.set('')
        return
    if right_dir == output_dir:
        self.messagebox.showinfo(title=I18n.tr('error.title.input'), message=I18n.tr('error.right_same_out'))
        self.outputname.set('')
        return
    if left_dir == right_dir:
        self.messagebox.showinfo(title=I18n.tr('error.title.input'), message=I18n.tr('error.left_same_right'))
        self._inputname.set('')
        return

    checks = tuple(int(var.get()) for var in check)
    if all(value == 0 for value in checks):
        self.messagebox.showinfo(title=I18n.tr('error.title.selection'), message=I18n.tr('error.select_set'))
        return

    _start_job(
        self,
        mes,
        btn,
        lambda report: collection_district(left_dir, right_dir, output_dir, checks, report),
    )


def duplicate_removel(input_dir, report):
    '''
    Remove duplicate images
    :param input_dir: image input directory
    :param report: log callback
    '''
    files = _image_files(input_dir)
    hist_dict = {}

    def handle(f):
        if is_duplicate_img(f, hist_dict):
            report(I18n.tr('log.duplicate_deleted', name=Load.name(f)))
        else:
            report(I18n.tr('log.no_duplicate'))

    _for_each(files, handle, report)
    report(I18n.tr('log.done'))


def scale_selecter(input_dir, output_dir, im_type, max_scale, min_scale, report):
    '''
    Copy images matching the aspect ratio
    :param input_dir: image input directory
    :param output_dir: image output path
    :param im_type: image type (all/landscape/portrait)
    :param max_scale: maximum aspect ratio
    :param min_scale: minimum aspect ratio
    :param report: log callback
    '''
    files = _image_files(input_dir)

    def handle(f):
        if im_type == Image.wh_type(f) or im_type == 0:
            if Image.wh_limitByPor(f, max_scale, min_scale):
                Load.full_copy(f, output_dir)
                report(I18n.tr('log.matched', name=Load.name(f)))
            else:
                report(I18n.tr('log.not_matched'))
        else:
            report(I18n.tr('log.not_matched'))

    _for_each(files, handle, report)
    report(I18n.tr('log.done'))


def limit_seleter(input_dir, output_dir, limit, report):
    '''
    Copy images matching the width and height limits
    :param input_dir: image input directory
    :param output_dir: image output path
    :param limit: width and height limits dictionary (maxH,minH,maxW,minW)
    :param report: log callback
    '''
    files = _image_files(input_dir)

    def handle(f):
        if Image.wh_limitByWH(f, limit):
            Load.full_copy(f, output_dir)
            report(I18n.tr('log.matched', name=Load.name(f)))
        else:
            report(I18n.tr('log.not_matched'))

    _for_each(files, handle, report)
    report(I18n.tr('log.done'))


def classify_selecter(input_dir, output_dir, checks, report):
    '''
    Classify images by type
    :param input_dir: image input directory
    :param output_dir: image output path
    :param checks: image types to include (landscape/portrait/square)
    :param report: log callback
    '''
    files = _image_files(input_dir)
    report(I18n.tr('log.processing'))

    if checks[0] == 1: Load.create_folder(output_dir + '/' + I18n.type_folder(1))
    if checks[1] == 1: Load.create_folder(output_dir + '/' + I18n.type_folder(2))
    if checks[2] == 1: Load.create_folder(output_dir + '/' + I18n.type_folder(0))

    def handle(f):
        im_type = Image.wh_type(f)
        Load.copy(f, output_dir, im_type)

    _for_each(files, handle, report)
    report(I18n.tr('log.done'))


def collection_district(left_dir, right_dir, output_dir, checks, report):
    '''
    Set operations: intersection, left difference, right difference, symmetric difference
    :param left_dir: left set input directory
    :param right_dir: right set input directory
    :param output_dir: image output path
    :param checks: set operation types
    :param report: log callback
    '''
    left_hist_dict = {}
    right_hist_dict = {}
    right_files = []
    report(I18n.tr('log.processing'))

    def add_left(f):
        left_hist_dict[str(Image.hist(f))] = f

    def add_right(f):
        right_hist_dict[str(Image.hist(f))] = f
        right_files.append(f)

    _for_each(_image_files(left_dir), add_left, report)
    _for_each(_image_files(right_dir), add_right, report)

    # intersection (dict)
    inter_dict = get_intersection(right_files, left_hist_dict)
    # left difference (list)
    left_list = get_difference(left_hist_dict, inter_dict)
    # right difference (list)
    right_list = get_difference(right_hist_dict, inter_dict)

    if checks[0] == 1:
        _for_each(
            inter_dict.values(),
            lambda f: Load._copy(f, output_dir + '/' + I18n.tr('folder.intersection') + '/'),
            report,
        )

    if checks[1] == 1:
        _for_each(
            left_list,
            lambda f: Load._copy(f, output_dir + '/' + I18n.tr('folder.left_diff') + '/'),
            report,
        )

    if checks[2] == 1:
        _for_each(
            right_list,
            lambda f: Load._copy(f, output_dir + '/' + I18n.tr('folder.right_diff') + '/'),
            report,
        )

    if checks[3] == 1:
        _for_each(
            left_list + right_list,
            lambda f: Load._copy(f, output_dir + '/' + I18n.tr('folder.symmetric_diff') + '/'),
            report,
        )

    report(I18n.tr('log.done'))
