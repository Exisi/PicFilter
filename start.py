import Load
import MyImg


def im_classify(f, output_path):
    if MyImg.wh_type(f):
        Load.copy(f, file_output=output_path, mode=1)
    else:
        Load.copy(f, file_output=output_path, mode=0)
    print(Load.name(f))


def Function(file_dir):
    Function = input("\n——————————>请选择: \n1.图片去重 \n2.去除黑白图片 \n3.根据长宽筛选出横竖屏图片 \n")
    if Function == "1":
        reImg_removal(file_dir)
    elif Function == "2":
        blackImg_removal(file_dir)
    elif Function == "3":
        whImg_Classify(file_dir)
    else:
        print("输入错误,请重新输入")
        main()


def reImg_removal(file_dir):
    Function(file_dir)


def blackImg_removal(file_dir):
    Function(file_dir)
 

def whImg_Classify(file_dir):
    '''
    :param file_dir: 图片目录
    :param output_path: 图片输出路径
    :param file_list: 图片路径
    '''
    output_path = input("请输入图片输出目录：")
    print("文件已读取")
    Load.create_folder(output_path)  # 新建输出路径
    file_list = Load.read(file_dir)  # 载入图片路径
    for f in file_list:
        if MyImg.is_img(f):
            im_classify(f, output_path)

    input("处理完成,按任意键继续")
    Function(file_dir)


def main():
    '''
    图片输入路径
    :param file_dir: 图片目录
    '''
    file_dir = input("请输入图片目录：")
    if Load.exists(file_dir):
        Function(file_dir)
    else:
        print("文件路目录不存在!请重试\n")
        main()


if __name__ == "__main__":
    main()
