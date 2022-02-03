import Filter
import webbrowser

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox


class App:
    def __init__(self):
        self.thread = 0
        self.root = tk.Tk()
        self.root.title('PicFilter')
        self.w, self.h = 500, 420
        self.inputname = tk.StringVar()
        self.outputname = tk.StringVar()
        self.scn_w, self.scn_h = self.root.maxsize()
        self.center_x = (self.scn_w - self.w) / 2
        self.center_y = (self.scn_h - self.h) / 2
        self.root.geometry('%dx%d+%d+%d' % (self.w, self.h, self.center_x, self.center_y))  # center window on desktop
        self.root.resizable(False, False)
        self.root.update_idletasks()
        self.root.deiconify()
        self.tab_bar()
        self.messagebox = messagebox

    def tab_bar(self):
        # 创建选项容器
        tabControl = ttk.Notebook(self.root)
        tab_first = ttk.Frame(master=tabControl)
        tabControl.add(tab_first, text='  图片去重  ')
        tab_second = ttk.Frame(tabControl)
        tabControl.add(tab_second, text='  比例限制  ')
        tab_third = ttk.Frame(tabControl)
        tabControl.add(tab_third, text='  宽高限制  ')
        tab_fourth = ttk.Frame(tabControl)
        tabControl.add(tab_fourth, text='  图片分类  ')
        tab_fifth = ttk.Frame(tabControl)
        tabControl.add(tab_fifth, text='  关于  ')
        tabControl.pack(expand=1, fill='both')
        self.fist_tab(tab_first)  # 载入第一个选择界面
        self.second_tab(tab_second)  # 载入第二个选择界面
        self.third_tab(tab_third)  # 载入第三个选择界面
        self.fourth_tab(tab_fourth)  # 载入第四个选择界面
        self.fifth_tab(tab_fifth)  # 载入第五个选择界面

    def fist_tab(self, tab):
        # 第一个选择界面
        lf = ttk.LabelFrame(tab, text=' tips: 图片去重会将您的重复图片删除')
        lf.grid(column=0, row=0, padx=5, pady=10)
        input_dir = ttk.Entry(lf, textvariable=self.inputname, width=50)
        input_dir.grid(column=0, row=0, sticky='W', padx=5, pady=5)
        input_dir.focus()
        source = ttk.Button(lf, text='输入', command=self.get_input_dir, takefocus=False)
        source.grid(column=1, row=0, sticky='W', padx=5, pady=5)
        mes = scrolledtext.ScrolledText(lf, width=50, state=tk.DISABLED, wrap='char')
        mes.grid(column=0, row=1, sticky='W', padx=5)
        btn_start = ttk.Button(lf, text='开始',
                               command=lambda: Filter.duplicate_start(self, mes, btn_start),
                               takefocus=False)
        btn_start.grid(column=1, row=1, sticky='N', padx=5)

    def second_tab(self, tab):
        # 第二个选择界面
        lf = ttk.LabelFrame(tab, text=' tips: 根据长宽比例筛选您的图片 ')
        lf.grid(column=0, row=0, padx=5, pady=10)
        input_dir = ttk.Entry(lf, textvariable=self.inputname, width=50)
        input_dir.grid(column=0, row=0, sticky='W', padx=5, pady=5)
        input_dir.focus()
        output_dir = ttk.Entry(lf, textvariable=self.outputname, width=50)
        output_dir.grid(column=0, row=1, sticky='W', padx=5)
        source = ttk.Button(lf, text='输入', command=self.get_input_dir)
        source.grid(column=1, row=0, sticky='W', padx=5, pady=5)
        output = ttk.Button(lf, text='输出', command=self.get_output_dir)
        output.grid(column=1, row=1, sticky='W', padx=5)
        lf_inner = ttk.Frame(lf)
        lf_inner.grid(column=0, row=2, sticky='W', padx=5, pady=5)
        label_min_scale = ttk.Label(lf_inner, text='最小长宽比')
        label_min_scale.grid(column=0, row=3, sticky='E', padx=5, pady=5)
        label_max_scale = ttk.Label(lf_inner, text='最大长宽比')
        label_max_scale.grid(column=3, row=3, sticky='E', padx=5, pady=5)
        min_scale = ttk.Spinbox(lf_inner, width=7, from_=1.0, to=2.0, format='%1.1f', increment=0.1,
                                validate='focusout', state='readonly')
        min_scale.grid(column=1, row=3, sticky='W', padx=5, pady=5)
        max_scale = ttk.Spinbox(lf_inner, width=7, from_=1.0, to=10.0, format='%1.1f', increment=0.1,
                                validate='focusout', state='readonly')
        max_scale.grid(column=4, row=3, sticky='W', padx=5, pady=5)
        type_label = ttk.Label(lf_inner, text='图片类型')
        type_label.grid(column=0, row=2, sticky='E', padx=5, pady=5)
        wh_type = ttk.Combobox(lf_inner, width=6, values=('全部', '横图', '竖图'), state='readonly')
        wh_type.current(0)
        wh_type.grid(column=1, row=2, sticky='W', padx=5, pady=5, ipadx=2)
        mes = scrolledtext.ScrolledText(lf, width=50, heigh=16, state=tk.DISABLED)
        mes.grid(column=0, row=4, sticky='W', padx=5)
        btn_start = ttk.Button(lf, text='开始',
                               command=lambda: Filter.scale_start(self, mes, btn_start, wh_type.current(),
                                                                  max_scale, min_scale))
        btn_start.grid(column=1, row=4, sticky='N', padx=5)

    def third_tab(self, tab):
        '''
        第三个选择界面
        :param validate: 绑定的输入验证函数
        :param limit: 图片宽高限制的字典(maxH,minH,maxW,minW)
        '''
        lf = ttk.LabelFrame(tab, text=' tips: 根据长宽临界大小筛选您的图片 ')
        lf.grid(column=0, row=0, padx=5, pady=10)
        input_dir = ttk.Entry(lf, textvariable=self.inputname, width=50)
        input_dir.grid(column=0, row=0, sticky='W', padx=5, pady=5)
        input_dir.focus()
        output_dir = ttk.Entry(lf, textvariable=self.outputname, width=50)
        output_dir.grid(column=0, row=1, sticky='W', padx=5)
        source = ttk.Button(lf, text='输入', command=self.get_input_dir)
        source.grid(column=1, row=0, sticky='W', padx=5, pady=5)
        output = ttk.Button(lf, text='输出', command=self.get_output_dir)
        output.grid(column=1, row=1, sticky='W', padx=5)
        lf_inner = ttk.Frame(lf)
        lf_inner.grid(column=0, row=2, sticky='W', padx=5, pady=5)
        w_max_label = ttk.Label(lf_inner, text='最大长度')
        w_max_label.grid(column=0, row=3, sticky='E', padx=5)
        h_max_label = ttk.Label(lf_inner, text='   最大宽度')
        h_max_label.grid(column=2, row=3, sticky='E', padx=5)
        w_min_label = ttk.Label(lf_inner, text='最小长度')
        w_min_label.grid(column=0, row=4, sticky='E', padx=5)
        h_min_label = ttk.Label(lf_inner, text='   最小宽度')
        h_min_label.grid(column=2, row=4, sticky='E', padx=5)
        validate = self.root.register(self.wh_value_validate)
        h_max_size = ttk.Spinbox(lf_inner, width=7, from_=0, to=99999, increment=1000, validate='focusout',
                                 validatecommand=(validate, '%P'))
        h_max_size.grid(column=1, row=3, sticky='W', padx=5, pady=5)
        w_max_size = ttk.Spinbox(lf_inner, width=7, from_=0, to=99999, increment=1000, validate='focusout',
                                 validatecommand=(validate, '%P'))
        w_max_size.grid(column=3, row=3, sticky='W', padx=5, pady=5)
        h_min_size = ttk.Spinbox(lf_inner, width=7, from_=0, to=99999, increment=1000, validate='focusout',
                                 validatecommand=(validate, '%P'))
        h_min_size.grid(column=1, row=4, sticky='W', padx=5, pady=5)
        w_min_size = ttk.Spinbox(lf_inner, width=7, from_=0, to=99999, increment=1000, validate='focusout',
                                 validatecommand=(validate, '%P'))
        w_min_size.grid(column=3, row=4, sticky='W', padx=5, pady=5)
        limit = {'maxH': h_max_size, 'minH': h_min_size, 'maxW': w_max_size, 'minW': w_min_size}
        mes = scrolledtext.ScrolledText(lf, width=50, heigh=16, state=tk.DISABLED)
        mes.grid(column=0, row=4, sticky='W', padx=5, ipady=1)
        btn_start = ttk.Button(lf, text='开始', command=lambda: Filter.limit_start(self, mes, btn_start, limit))
        btn_start.grid(column=1, row=4, sticky='N', padx=5)

    def fourth_tab(self, tab):
        '''
        第四个选择界面
        :param check: (addH,addW,addS) 图片类型复选框是否选中的值
        '''
        lf = ttk.LabelFrame(tab, text=' tips: 对您的图片进行横/竖/方的图片类型分类')
        lf.grid(column=0, row=0, padx=5, pady=10)
        input_dir = ttk.Entry(lf, textvariable=self.inputname, width=50)
        input_dir.grid(column=0, row=0, sticky='W', padx=5, pady=5)
        input_dir.focus()
        output_dir = ttk.Entry(lf, textvariable=self.outputname, width=50)
        output_dir.grid(column=0, row=1, sticky='W', padx=5)
        source = ttk.Button(lf, text='输入', command=self.get_input_dir)
        source.grid(column=1, row=0, sticky='W', padx=5, pady=5)
        output = ttk.Button(lf, text='输出', command=self.get_output_dir)
        output.grid(column=1, row=1, sticky='W', padx=5)
        lf_inner = ttk.Frame(lf)
        lf_inner.grid(column=0, row=2, sticky='W', padx=5, pady=5)
        addH = tk.IntVar()
        addW = tk.IntVar()
        addS = tk.IntVar()
        check = [addH, addW, addS]
        w_check = tk.Checkbutton(lf_inner, text='横图', variable=addH)
        h_check = tk.Checkbutton(lf_inner, text='竖图', variable=addW)
        square_check = tk.Checkbutton(lf_inner, text='方图', variable=addS)
        w_check.grid(column=0, row=0, sticky='W', padx=5, pady=5)
        h_check.grid(column=1, row=0, sticky='W', padx=5, pady=5)
        square_check.grid(column=2, row=0, sticky='W', padx=5, pady=5)
        w_check.select()
        h_check.select()
        square_check.select()
        mes = scrolledtext.ScrolledText(lf, width=50, heigh=18, state=tk.DISABLED)
        mes.grid(column=0, row=4, sticky='W', padx=5, ipady=1)
        btn_start = ttk.Button(lf, text='开始', command=lambda: Filter.classify_start(self, mes, btn_start, check))
        btn_start.grid(column=1, row=4, sticky='N', padx=5)

    def fifth_tab(self, tab):
        # 第五个选择界面
        lf = ttk.Frame(tab)
        lf.grid(column=0, row=0, padx=5, pady=10)
        label = ttk.Label(lf, text='PicFilter 0.5')
        label.grid(column=0, row=0, padx=5, pady=5, sticky='W')
        label = ttk.Label(lf, text='项目地址：')
        label.grid(column=0, row=2, pady=5, sticky='E', )
        btn_source = tk.Button(lf, text='https://github.com/Exisi/PicFilter', bd=0, fg='blue', takefocus=False,
                               activeforeground='red', cursor='plus', justify='left', command=self.direct_project)
        btn_source.grid(column=1, row=2, pady=5, sticky='W', )

    def wh_value_validate(self, value):
        '''
        宽高值的输入验证
        :param value: 输入的值
        :return: bool
        '''
        if value.isdigit():
            return True
        elif value != '':
            messagebox.showinfo(title='输入错误', message='请输入正整数数字！')
            return False

    def direct_project(self):
        # 关于项目的跳转
        webbrowser.open('https://github.com/Exisi/PicFilter')

    def get_input_dir(self):
        # 获取文件输入路径选择的值，传递给输入框
        indir = tk.filedialog.askdirectory()
        self.inputname.set(indir)

    def get_output_dir(self):
        # 获取文件输出路径选择的值，传递给输入框
        outdir = tk.filedialog.askdirectory()
        self.outputname.set(outdir)


if __name__ == '__main__':
    app = App()
    app.root.mainloop()
