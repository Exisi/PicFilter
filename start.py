import Function
import MyImg

def im_classify(f, output_path):
    if MyImg.wh_type(f):
        Function.copy(f, file_output=output_path, mode=1)
    else:
        Function.copy(f, file_output=output_path, mode=0)
    print(Function.name(f))

def main():
    #载入图片
    file_dir=input("请输入图片目录：")
    output_path=input("请输入图片输出目录：")
    if Function.exists(file_dir):
        print("文件已读取")
        Function.create_folder(output_path)
        file_list=Function.read(file_dir)
        for f in file_list:

            if MyImg.is_img(f):
                im_classify(f, output_path)

        input("处理完成，输入任意键退出")
    else:
        print("文件路目录不存在!")

if __name__ == "__main__":
    main()
