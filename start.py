import Load
import MyImg

def im_classify(f, output_path):
    if MyImg.wh_type(f):
        Load.copy(f, file_output=output_path, mode=1)
    else:
        Load.copy(f, file_output=output_path, mode=0)
    print(Load.name(f))

def main():
    #载入图片
    file_dir=input("请输入图片目录：")
    output_path=input("请输入图片输出目录：")
    if Load.exists(file_dir):
        print("文件已读取")
        Load.create_folder(output_path)
        file_list=Load.read(file_dir)
        for f in file_list:
            if MyImg.is_img(f):
                im_classify(f, output_path)
    else:
        print("文件路目录不存在!")

    input("处理完成，输入任意键退出")

if __name__ == "__main__":
    main()
