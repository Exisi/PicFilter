import Load
import MyImg


def Function(files):
    '''
    :param files: 图片列表
    '''
    Func = input("\n——————————>请选择: \n"
                 "1.图片去重 \n2.筛选横竖屏图片 \nEsc:[Enter] <————\n")
    if Func == "1":
        reImg_removal(files)
    elif Func == "2":
        whImg_Classify(files)
    elif Func == "":
        exit()
    else:
        print("输入错误,请重新输入")
        main()


def im_classify(f, output_path):
    '''
    输出分类后的图片
    :param f: 图片路径
    :param output_path: 输出目录
    '''
    if MyImg.wh_type(f) == 1:
        Load.copy(f, file_output=output_path, mode=1)
    elif MyImg.wh_type(f) == 2:
        Load.copy(f, file_output=output_path, mode=2)
    else:
        Load.copy(f, file_output=output_path, mode=0)
    print(Load.name(f))


def reImg_removal(files):
    '''
    图片去重，利用字典和图片像素直方图的唯一值，确定重复
    :param files: 图片列表
    '''
    hist_dict = {}
    for f in files:
        if str(MyImg.hist(f)) not in hist_dict:
            print("Not repeat, skip")
            hist_dict[str(MyImg.hist(f))] = f
        else:
            print(f, "存在重复，已删除")
            Load.delete(f)
    input("\n处理完成,按任意键继续")
    Function(files)


def whImg_Classify(files):
    '''
    筛选横竖屏图片
    :param files: 图片列表
    :param f: 图片路径
    '''
    output_path = input("请输入图片输出目录：")
    if output_path != " " and output_path != "":
        Load.create_folder(output_path)  # 新建输出路径
    else:
        print("输出目录不能为空,请重新输入")
        Function(files)
    print("文件已读取")
    for f in files:
        if MyImg.is_img(f):
            im_classify(f, output_path)
    input("处理完成,按任意键继续")
    Function(files)


def main():
    '''
    图片输入路径
    :param file_dir: 图片目录
    :param files 所有图片路径
    '''
    file_dir = input("请输入图片目录：")
    if Load.exists(file_dir):
        files = Load.read(file_dir)  # 载入图片路径
        Function(files)
    else:
        print("文件路目录不存在!请重试\n")
        main()


if __name__ == "__main__":
    main()
