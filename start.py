import Load
import MyImg


def Function(files):
    Function = input("\n——————————>请选择: \n"
                     "1.图片去重 \n2.去除黑白图片 \n3.筛选横竖屏图片 \nEsc:[Enter] <————\n")
    if Function == "1":
        reImg_removal(files)
    elif Function == "2":
        grayImg_removal(files)
    elif Function == "3":
        whImg_Classify(files)
    elif Function == "":
        exit()
    else:
        print("输入错误,请重新输入")
        main()


def im_classify(f, output_path):
    '''
    :param f: 图片路径
    :param output_path: 输出目录
    '''

    if MyImg.wh_type(f):
        Load.copy(f, file_output=output_path, mode=1)
    else:
        Load.copy(f, file_output=output_path, mode=0)
    print(Load.name(f))


def reImg_removal(files):
    Function(files)


def grayImg_removal(files):
    Function(files)


def whImg_Classify(files):
    '''
    :param files: 图片列表
    :param f: 图片路径
    '''
    output_path = input("请输入图片输出目录：")
    Load.create_folder(output_path)  # 新建输出路径
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
