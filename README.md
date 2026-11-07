
<p align="center">
  <img src="/doc/images/favicon.ico" width="50">
</p>

<p align="center">PicFilter 是一个简单的图片处理程序，基于 Pillow 实现，适用于批处理大量图片的筛选。</p>

<p align="center">
  <strong>简体中文</strong> | <a href="README.en.md">English</a>
</p>

<p align="center">
  <img src="/doc/images/cover.png">
</p>

# 功能

- 图片去重：基于像素直方图识别重复图片
- 宽高比筛选：按最小/最大宽高比筛选图片
- 宽高值筛选：按最小/最大宽度和高度筛选图片
- 图片分类：自动分类为横图、竖图、方图
- 集合选取：对两组图片求交集、左右差集和对称差集

# 技术栈

- CustomTkinter
- Pillow
- Tkinter

# 项目结构

```text
PicFilter/
├─ App.py                  # 程序入口与主界面
├─ filter/
│  ├─ Filter.py            # 去重、筛选、分类与集合运算
│  ├─ Load.py              # 文件遍历、复制与目录创建
│  └─ Image.py             # 图片识别、尺寸判断与直方图
├─ utils/
│  ├─ I18n.py              # 多语言加载与系统语言检测
│  ├─ Icon.py              # 内嵌应用图标
│  └─ Settings.py          # 用户偏好持久化
├─ languages/
│  ├─ zh.json              # 中文文案
│  └─ en.json              # 英文文案
├─ assets/
│  └─ icons/               # 界面图标（亮色/暗色）
├─ doc/
│  └─ images/              # README 截图与应用图标
├─ installer/              # 安装包相关文件
├─ scripts/                # 辅助脚本
├─ .github/workflows/      # CI 配置
├─ package.json            # 版本号与项目元数据
├─ requirements.txt        # Python 依赖
├─ README.md               # 中文说明
├─ README.en.md            # English documentation
└─ LICENSE                 # MIT License
```

# 启动

```bash
pip install -r requirements.txt
python App.py
```

# 使用注意

- 图片去重暂不支持不同尺寸的相同图片判断
- 去重会直接删除重复图片，操作前请先备份重要文件
- 比例/尺寸筛选和分类会将通过的图片复制到输出目录，源文件不会删除
- 输入目录和输出目录不能相同

# 许可证

本项目基于 [MIT License](LICENSE) 开源。
