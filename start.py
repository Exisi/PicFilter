import Load
import MyImg


def Function(files):
    '''
    :param files: 图片列表
    '''
    Func = input('\n——————————>请选择: \n'
                 '1.图片去重 \n2.宽高限制 \n3.筛选横竖屏图片 \nEsc:[Enter] <————\n')
    if Func == '1':
        reImg_removal(files)
    elif Func == '2':
        whImg_limit(files)
    elif Func == '3':
        whImg_Classify(files)
    elif Func == '':
        exit()
    else:
        print('输入错误,请重新输入')
        main()


def whImg_limit_whsetting(type, files):
    '''
    :param type: 图片类型
    :param limit: 最大最小宽高限制
    :return: dict
    '''
    limit = {}
    try:
        if type == '1':
            limit['maxH'] = abs(int(input('最大高度: ')))
            return limit
        elif type == '2':
            limit['maxW'] = abs(int(input('最大宽度: ')))
            return limit
        else:
            limit['maxW'] = abs(int(input('最大宽度: ')))
            limit['minW'] = abs(int(input('最小宽度: ')))
            limit['maxH'] = abs(int(input('最大高度: ')))
            limit['minH'] = abs(int(input('最小高度: ')))
            return limit
    except:
        print('输入错误,请重新输入')
        Function(files)


def whImg_limit(files):
    '''
    图片限制宽高，模式1.使用宽高比，2.使用纯宽高数据
    :param pro: 输入的宽高比
    :param files: 图片列表
    :param limit: 最大最小宽高限制
    :param im_type: 图片类型
    :param proprotion: 宽高比
    '''
    proprotion = 1.1  # 默认宽高比
    try:
        por = input('是否按比例限制(默认y)？(y/n)')
        if por == 'n':
            mode = 0
            use_type = input('是否指定图片类型(默认y)？(y/n)')
            if use_type == 'n':
                im_type = '0'
            else:
                im_type = input('图片类型(默认2): \n1.竖图 \n2.横图 \n')
                if im_type != '1' and im_type != '2' and im_type != '0': im_type = '2'
        else:
            mode = 1
            pro = input('宽高比(默认1.1): ')
            if pro != '' and float(pro) > 1.1:
                proprotion = float(pro)
            im_type = input('图片类型(默认2): \n1.竖图 \n2.横图 \n')

            if im_type != '1' and im_type != '2': im_type = '2'
    except:
        print('输入错误，请重试')
        Function(files)
    else:
        if mode == 0:
            limit = whImg_limit_whsetting(im_type, files)
            for f in files:
                result = MyImg.wh_limitByWH(f, limit, im_type)
                if result:
                    print('sucess,skip ,file: ', f)
                else:
                    print('不符合，已移除, 文件名:', f)
                    Load.move(f)
        else:
            for f in files:
                result = MyImg.wh_limitByPor(f, im_type, proprotion)
                if result:
                    print('sucess,skip ,file: ', f)
                else:
                    print('不符合，已移除, 文件名:', f)
                    Load.move(f)
        input('\n处理完成,按任意键继续')
        Function(files)


def im_classify(f, output_path):
    '''
    输出分类后的图片
    :param f: 图片路径
    :param output_path: 输出目录
    '''
    if MyImg.wh_type(f) == 1:
        Load.copy(f, file_output=output_path, mode=1)
        print('[ type: horizon ] ==> file:', Load.name(f))
    elif MyImg.wh_type(f) == 2:
        Load.copy(f, file_output=output_path, mode=2)
        print('[ type: vertical ] ==> file:', Load.name(f))
    else:
        Load.copy(f, file_output=output_path, mode=0)
        print('[ type: square ] ==> file:', Load.name(f))


def reImg_removal(files):
    '''
    图片去重，利用字典和图片像素直方图的唯一值，确定重复
    :param files: 图片列表
    '''
    hist_dict = {}
    for f in files:
        if str(MyImg.hist(f)) not in hist_dict:
            print('Not repeat, skip')
            hist_dict[str(MyImg.hist(f))] = f
        else:
            print(f, '存在重复，已删除')
            Load.delete(f)
    input('\n处理完成,按任意键继续')
    Function(files)


def whImg_Classify(files):
    '''
    筛选横竖屏图片
    :param files: 图片列表
    :param f: 图片路径
    '''
    output_path = input('请输入图片输出目录：')
    if output_path != " " and output_path != "":
        Load.create_folder(output_path)  # 新建输出路径
    else:
        print('输出目录不能为空,请重新输入')
        Function(files)
    print('文件已读取')
    for f in files:
        if MyImg.is_img(f):
            im_classify(f, output_path)
    input('处理完成,按任意键继续')
    Function(files)


def main():
    '''
    图片输入路径
    :param file_dir: 图片目录
    :param files 所有图片路径
    '''
    file_dir = input('请输入图片目录：')
    if Load.exists(file_dir):
        files = Load.read(file_dir)  # 载入图片路径
        Function(files)
    else:
        print('文件路目录不存在!请重试\n')
        main()


if __name__ == "__main__":
    main()
