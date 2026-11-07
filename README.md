![PicFilter](https://socialify.git.ci/Exisi/PicFilter/image?description=1&forks=1&issues=1&language=1&name=1&owner=1&pattern=Plus&stargazers=1&theme=Light)

PicFilter是一个简单的图片处理程序，基于Pillow的实现，适用于批处理大量图片的筛选

# 功能
* 图片去重
* 宽高比筛选
* 宽高值筛选
* 分类为横/竖/方形图片
* 两图片组之间的集合选取对比


# 界面
使用 CustomTkinter 构建

<img src="https://raw.githubusercontent.com/Exisi/PicFilter/main/doc/img/show/1.jpg" width=500>

# 使用注意
* 图片去重暂不支持不同大小的相同图片的判断
* 通过筛选的图片会复制到符合的图片目录中
* 图片筛选后的源文件不会删除（图片去重除外）

# 构建与发布

```bash
pip install -r requirements.txt
python App.py
```

版本号统一保存在 `package.json` 中，程序启动时会读取该文件。

推送 `v<major>.<minor>.<patch>` 格式的 tag 会触发 GitHub Actions：同步版本号，在 Windows、Linux、macOS 上构建安装包与便携版，并根据上一个 tag 到当前 tag 之间的提交生成更新说明，自动发布到 GitHub Releases。

| 平台 | 安装包 | 便携版 |
| --- | --- | --- |
| Windows x64 | `PicFilter-v*-windows-x64-setup.exe` | `PicFilter-v*-windows-x64-portable.zip` |
| Linux x64 | `PicFilter-v*-linux-x64.deb` | `PicFilter-v*-linux-x64-portable.tar.gz` |
| macOS Apple Silicon | `PicFilter-v*-macos-arm64.dmg` | `PicFilter-v*-macos-arm64-portable.zip` |
| macOS Intel | `PicFilter-v*-macos-x64.dmg` | `PicFilter-v*-macos-x64-portable.zip` |

macOS 安装包未签名，首次打开需右键选择「打开」，或执行 `xattr -dr com.apple.quarantine /Applications/PicFilter.app` 后再启动。

```bash
git tag v0.3.2
git push origin v0.3.2
```

