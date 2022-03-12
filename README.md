# PicFilter
## 前言
基于Pillow的图片筛选，因为找不到合适的图片筛选工具，就自己写了XD

* 图片去重
* 宽高比筛选
* 宽高值筛选
* 分类为横/竖/方形图片

#### 注
* 图片去重暂不支持不同大小的相同图片的判断
* 通过筛选的图片会复制到符合的图片目录中
* 图片筛选后的源文件不会删除（图片去重除外）

|||||
|-|-|-|-|
|![](https://raw.githubusercontent.com/Exisi/PicFilter/main/img/show/1.jpg)|![](https://raw.githubusercontent.com/Exisi/PicFilter/main/img/show/2.jpg)|![](https://raw.githubusercontent.com/Exisi/PicFilter/main/img/show/3.jpg)|![](https://raw.githubusercontent.com/Exisi/PicFilter/main/img/show/4.jpg)|
|||||

## 更新
#### V0.6
1. 优化了获取图片路径的速度
2. 解决存在子文件夹时，对其他文件夹图片不处理的问题

#### V0.5
1. 更新GUI界面支持
2. 修改和调整了部分代码
3. 对图片源文件不再删除（图片去重除外），符合筛选结果的图片将会复制到新文件中（符合的图片）

#### V0.4
1. 更新对图片的宽高排除，支持宽高比和纯宽高数据
2. 对排除的图片另外添加移除目录，防止误删

#### V0.3
1. 更新对方形图的分类

#### V0.2
1. 支持重复图片的简单去除，适用于由同一个文件复制出的图片去除

#### V0.1
1. 根据长宽筛选，分类为横竖屏图片

