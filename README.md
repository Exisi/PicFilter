![PicFilter](https://socialify.git.ci/Exisi/PicFilter/image?description=1&forks=1&issues=1&language=1&name=1&owner=1&pattern=Plus&stargazers=1&theme=Light)

PicFilter是一个简单的图片处理程序，基于Pillow的实现，适用于批处理大量图片的筛选

# 功能
* 图片去重
* 宽高比筛选
* 宽高值筛选
* 分类为横/竖/方形图片
* 两图片组之间的集合选取对比

||||||
|-|-|-|-|-|
|![](https://raw.githubusercontent.com/Exisi/PicFilter/main/img/show/1.jpg)|![](https://raw.githubusercontent.com/Exisi/PicFilter/main/img/show/2.jpg)|![](https://raw.githubusercontent.com/Exisi/PicFilter/main/img/show/3.jpg)|![](https://raw.githubusercontent.com/Exisi/PicFilter/main/img/show/4.jpg)|![](https://raw.githubusercontent.com/Exisi/PicFilter/main/img/show/5.jpg)|
||||||

# 使用注意
* 图片去重暂不支持不同大小的相同图片的判断
* 通过筛选的图片会复制到符合的图片目录中
* 图片筛选后的源文件不会删除（图片去重除外）
* 仅支持对 (jpg, bmp, png, jpeg, gif, webp, ico) 图片类型的处理
