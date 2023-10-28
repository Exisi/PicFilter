import Load
import MyImg
from threading import Thread


def os_exist(in_dir, out_dir):
    '''
    判断图片输入输出路径是否存在
    :param in_dir: 图片输入目录
    :param out_dir 图片输出路径
    '''
    if out_dir is None:
        out_dir = in_dir
    if Load.exists(in_dir) and Load.exists(out_dir):
        return True
    else:
        return False


def is_duplicate_img(f, hist_dict):
    '''
    图片去重，利用字典和图片像素直方图的唯一值，确定重复
    :param files: 图片列表
    '''
    hist = str(MyImg.hist(f))
    if hist not in hist_dict:
        hist_dict[hist] = f
        return False
    else:
        Load.delete(f)
        return True


def get_intersection(files, hist_dict):
    '''
    取出图片集合间的交集
    :param files: 图片列表
    :param hist_dict: 图片列表直方图数组
    :param inter_hist_dict: 交集集合字典
    :return: dict
    '''
    inter_hist_dict = {}
    for f in files:
        hist = str(MyImg.hist(f))
        if (hist in hist_dict):
            inter_hist_dict[hist] = f
    return inter_hist_dict


def get_difference(hist_dict, inter_dict):
    '''
    获取单个集合的差集
    :param hist_dict: 左集合的图片直方图字典
    :param inter_dict: 差集
    :return: list
    '''
    diff_dict = []
    for hist in hist_dict:
        if hist not in inter_dict:
            diff_dict.append(hist_dict[hist])
    return diff_dict


def duplicate_start(self, mes, btn):
    '''
    图片去重的启动方法，检测输入的值是否正确
    :param self: GUI.App类属性
    :param mes: GUI.fist_tab.scrolledtext 程序运行的提示信息
    :param btn: GUI.fist_tab.Button 开始按钮
    '''
    btn['state'] = 'disable'
    if os_exist(self.inputname.get(), None):
        t1 = Thread(target=duplicate_removel, args=(self, mes, btn))
        t1.start()
    else:
        self.messagebox.showinfo(title='输入错误', message='文件路径不存在，请重新选择')
        self.inputname.set('')
        btn['state'] = 'normal'


def scale_start(self, mes, btn, im_type, max_scale, min_scale):
    '''
    长宽比限制筛选的启动方法，检测输入的值是否正确
    :param self: GUI.App类属性
    :param mes: GUI.second_tab.scrolledtext 程序运行的提示信息
    :param btn: GUI.second_tab.Button 开始按钮
    :param im_type: 图片类型（全部/横图/竖图）
    :param max_scale: 图片最大长宽比
    :param min_scale: 图片最小长宽比
    '''
    btn['state'] = 'disable'
    if os_exist(self.inputname.get(), self.outputname.get()):
        if self.inputname.get() == self.outputname.get():
            self.messagebox.showinfo(title='输入错误', message='文件输入路径与输出路径不能相同，请重新选择！')
            self.outputname.set('')
            btn['state'] = 'normal'
        else:
            if max_scale.get() == '' or min_scale.get() == '':
                self.messagebox.showinfo(title='输入错误', message='长宽比不能未空！')
                btn['state'] = 'normal'
            elif float(max_scale.get()) < float(min_scale.get()):
                self.messagebox.showinfo(title='输入错误', message='最大长宽比不能小于最小长宽比！')
                btn['state'] = 'normal'
            else:
                t1 = Thread(target=scale_selecter,
                            args=(self, mes, btn, im_type, float(max_scale.get()), float(min_scale.get())))
                t1.start()
    else:
        self.messagebox.showinfo(title='输入错误', message='文件路径不存在，请重新选择！')
        self.inputname.set('')
        self.outputname.set('')
        btn['state'] = 'normal'


def limit_start(self, mes, btn, limit):
    '''
    长宽大小限制的启动方法，检测输入的值是否正确
    :param self: GUI.App类属性
    :param mes: GUI.third_tab.scrolledtext 程序运行的提示信息
    :param btn: GUI.third_tab.Button 开始按钮
    :param limit: 图片宽高限制的字典(maxH,minH,maxW,minW)
    '''
    btn['state'] = 'disable'
    if os_exist(self.inputname.get(), self.outputname.get()):
        if self.inputname.get() == self.outputname.get():
            self.messagebox.showinfo(title='输入错误', message='文件输入路径与输出路径不能相同，请重新选择！')
            self.outputname.set('')
            btn['state'] = 'normal'
        else:
            text = limit['maxH'].get() + limit['minH'].get() + limit['maxW'].get() + limit['minW'].get()
            if limit['maxH'].get() == '' or limit['minH'].get() == '' or limit['maxW'].get() == '' or limit[
                'minW'].get() == '':
                self.messagebox.showinfo(title='输入错误', message='输入内容不能为空！')
                btn['state'] = 'normal'
            else:
                if text.isdigit():
                    if float(limit['maxH'].get()) < float(limit['minH'].get()) or float(limit['maxW'].get()) < float(
                            limit['minW'].get()):
                        self.messagebox.showinfo(title='输入错误', message='最大值不能小于最小值！')
                        btn['state'] = 'normal'
                    else:
                        if float(limit['maxH'].get()) > 99999 or float(limit['minH'].get()) > 99999 or float(
                                limit['maxW'].get()) > 99999 or float(limit['minW'].get()) > 99999:
                            self.messagebox.showinfo(title='输入错误', message='数值过大！')
                            btn['state'] = 'normal'
                        else:
                            t1 = Thread(target=limit_seleter, args=(self, mes, btn, limit))
                            t1.start()
                else:
                    self.messagebox.showinfo(title='输入错误', message='输入内容必须为正整数数字！')
                    btn['state'] = 'normal'
    else:
        self.messagebox.showinfo(title='输入错误', message='文件路径不存在，请重新选择！')
        self.inputname.set('')
        self.outputname.set('')
        btn['state'] = 'normal'


def classify_start(self, mes, btn, check):
    '''
    图片分类的启动方法，检测输入的值是否正确
    :param self: GUI.App类属性
    :param mes: GUI.fourth_tab.scrolledtext 程序运行的提示信息
    :param btn: GUI.fourth_tab.Button 开始按钮
    :param check: 图片类型是否选择（方图/横图/竖图）
    '''
    btn['state'] = 'disable'
    if os_exist(self.inputname.get(), self.outputname.get()):
        if self.inputname.get() == self.outputname.get():
            self.messagebox.showinfo(title='输入错误', message='文件输入路径与输出路径不能相同，请重新选择！')
            self.outputname.set('')
            btn['state'] = 'normal'
        else:
            if check[0].get() == check[1].get() == check[2].get() == 0:
                self.messagebox.showinfo(title='选择错误', message='请至少选择一种图片类型！')
                btn['state'] = 'normal'
            else:
                t1 = Thread(target=classify_selecter, args=(self, mes, btn, check))
                t1.start()
    else:
        self.messagebox.showinfo(title='输入错误', message='文件路径不存在，请重新选择！')
        self.inputname.set('')
        self.outputname.set('')
        btn['state'] = 'normal'


def collection_start(self, mes, btn, check):
    '''
    图片分类的启动方法，检测输入的值是否正确
    :param self: GUI.App类属性
    :param mes: GUI.fourth_tab.scrolledtext 程序运行的提示信息
    :param btn: GUI.fourth_tab.Button 开始按钮
    :param check: (inter,l_diff,r_diff,lr_diff) 集合选区的类型
    '''
    btn['state'] = 'disable'
    if os_exist(self.inputname.get(), self.outputname.get()) and os_exist(self._inputname.get(), None):
        if self.inputname.get() == self.outputname.get():
            self.messagebox.showinfo(title='输入错误', message='文件左输入路径和输出路径不能相同，请重新选择！')
            self.outputname.set('')
            btn['state'] = 'normal'
        elif self._inputname.get() == self.outputname.get():
            self.messagebox.showinfo(title='输入错误', message='文件右输入路径和输出路径不能相同，请重新选择！')
            self.outputname.set('')
            btn['state'] = 'normal'
        elif self.inputname.get() == self._inputname.get():
            self.messagebox.showinfo(title='输入错误', message='文件左输入路径和右输入路径不能相同，请重新选择！')
            self._inputname.set('')
            btn['state'] = 'normal'
        else:
            if check[0].get() == check[1].get() == check[2].get() == check[3].get() == 0:
                self.messagebox.showinfo(title='选择错误', message='请至少选择一种集合区间！')
                btn['state'] = 'normal'
            else:
                pass
                t1 = Thread(target=collection_district, args=(self, mes, btn, check))
                t1.start()
    else:
        self.messagebox.showinfo(title='输入错误', message='文件路径不存在，请重新选择！')
        self.inputname.set('')
        self._inputname.set('')
        self.outputname.set('')
        btn['state'] = 'normal'


def duplicate_removel(self, mes, btn):
    '''
    移除重复的图片
    :param self: GUI.App类属性
    :param mes: GUI.fist_tab.scrolledtext 程序运行的提示信息
    :param btn: GUI.fist_tab.Button 开始按钮
    '''
    files = Load.read(self.inputname.get())
    files = [f for f in files if MyImg.is_img(f)]
    hist_dict = {}
    mes['state'] = 'normal'
    mes.delete('1.0', 'end')
    for f in files:
        if is_duplicate_img(f, hist_dict):
            mes.insert('end', '[ ' + Load.name(f) + ' ] - 重复，已删除\n\n')
        else:
            mes.insert('end', '无重复，下一张\n\n')
        mes.see('end')
        self.update_idletasks()
    mes.insert('end', '处理完成！')
    mes['state'] = 'disable'
    mes.see('end')
    btn['state'] = 'normal'


def scale_selecter(self, mes, btn, im_type, max_scale, min_scale):
    '''
    筛选出符合长宽比的图片
    :param self: GUI.App类属性
    :param mes: GUI.second_tab.scrolledtext 程序运行的提示信息
    :param btn: GUI.second_tab.Button 开始按钮
    :param im_type: 图片类型（全部/横图/竖图）
    :param max_scale: 最大长宽比
    :param min_scale: 最小长宽比
    '''
    files = Load.read(self.inputname.get())
    files = [f for f in files if MyImg.is_img(f)]
    mes['state'] = 'normal'
    mes.delete('1.0', 'end')
    for f in files:
        if im_type == MyImg.wh_type(f) or im_type == 0:
            if MyImg.wh_limitByPor(f, max_scale, min_scale):
                Load.full_copy(f, self.outputname.get())
                mes.insert('end', '[ ' + Load.name(f) + ' ] - 符合，已加入\n\n')
            else:
                mes.insert('end', '不符合，下一张\n\n')
        else:
            mes.insert('end', '不符合，下一张\n\n')
        mes.see('end')
        self.update_idletasks()
    mes.insert('end', '处理完成！')
    mes['state'] = 'disable'
    mes.see('end')
    btn['state'] = 'normal'


def limit_seleter(self, mes, btn, limit):
    '''
    筛选出符合最大最小长宽值的图片
    :param self: GUI.App类属性
    :param mes: GUI.third_tab.scrolledtext 程序运行的提示信息
    :param btn: GUI.third_tab.Button 开始按钮
    :param limit: 图片宽高限制的字典(maxH,minH,maxW,minW)
    '''
    files = Load.read(self.inputname.get())
    files = [f for f in files if MyImg.is_img(f)]
    mes['state'] = 'normal'
    mes.delete('1.0', 'end')
    for f in files:
        if MyImg.wh_limitByWH(f, limit):
            Load.full_copy(f, self.outputname.get())
            mes.insert('end', '[ ' + Load.name(f) + ' ] - 符合，已加入\n\n')
        else:
            mes.insert('end', '不符合，下一张\n\n')
        mes.see('end')
        self.update_idletasks()
    mes.insert('end', '处理完成！')
    mes['state'] = 'disable'
    mes.see('end')
    btn['state'] = 'normal'


def classify_selecter(self, mes, btn, check):
    '''
    图片类型分类
    :param self: GUI.App类属性
    :param mes: GUI.fourth_tab.scrolledtext 程序运行的提示信息
    :param btn: GUI.fourth_tab.Button 开始按钮
    :param im_type: 图片类型（方图/横图/竖图）
    '''
    files = Load.read(self.inputname.get())
    files = [f for f in files if MyImg.is_img(f)]
    mes['state'] = 'normal'
    mes.delete('1.0', 'end')
    mes.insert('end', '处理中...\n\n')

    if check[0].get() == 1: Load.create_folder(self.outputname.get() + '/横图')
    if check[1].get() == 1: Load.create_folder(self.outputname.get() + '/竖图')
    if check[2].get() == 1: Load.create_folder(self.outputname.get() + '/方图')
    for f in files:
        im_type = MyImg.wh_type(f)
        Load.copy(f, self.outputname.get(), im_type)
    mes.insert('end', '处理完成！')
    mes['state'] = 'disable'
    mes.see('end')
    btn['state'] = 'normal'


def collection_district(self, mes, btn, check):
    '''
    图片类型分类
    :param self: GUI.App类属性
    :param mes: GUI.fourth_tab.scrolledtext 程序运行的提示信息
    :param btn: GUI.fourth_tab.Button 开始按钮
    :param check: 集合选区类型
    :return:
    '''
    left_files = Load.read(self.inputname.get())
    right_files = Load.read(self._inputname.get())
    left_files = [f for f in left_files if MyImg.is_img(f)]
    right_files = [f for f in right_files if MyImg.is_img(f)]
    mes['state'] = 'normal'
    mes.delete('1.0', 'end')
    mes.insert('end', '处理中...\n\n')

    left_hist_dict = {}
    right_hist_dict = {}

    for lf in left_files:
        hist = str(MyImg.hist(lf))
        left_hist_dict[hist] = lf

    for lf in right_files:
        hist = str(MyImg.hist(lf))
        right_hist_dict[hist] = lf
    # 交集(字典)
    inter_dict = get_intersection(right_files, left_hist_dict)
    # 左差集(列表)
    left_list = get_difference(left_hist_dict, inter_dict)
    # 右差集(列表)
    right_list = get_difference(right_hist_dict, inter_dict)

    if check[0].get() == 1:
        for f in inter_dict:
            Load._copy(inter_dict[f], self.outputname.get() + '/交集/')

    if check[1].get() == 1:
        for f in left_list:
            Load._copy(f, self.outputname.get() + '/左差集/')

    if check[2].get() == 1:
        for f in right_list:
            Load._copy(f, self.outputname.get() + '/右差集/')

    if check[3].get() == 1:
        double_list = left_list + right_list
        for f in double_list:
            Load._copy(f, self.outputname.get() + '/对称差集/')

    mes.insert('end', '处理完成！')
    mes['state'] = 'disable'
    mes.see('end')
    btn['state'] = 'normal'
