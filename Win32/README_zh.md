# TopixPop Win32

Windows平台~~量身定做~~的TopixPop版本

# DEV5：

1. 根据当前位置的日出和日落时间更改墙纸的背景颜色

2. 自动设置壁纸分辨率

# 部署

## Windows 10

1. 安装Python> = 3.7，包括pip

2. 运行Command（Win + R，键入CMD），进入目录" TopixPop / Win32"，然后在控制台中输入 `pip install -r requirements.txt`

3. 运行（双击）"mGenerate.pyw"

## Windows NT 6（Windows 7，Windows 8.1）

1. 安装Python == 3.8（必须为Python 3.8.X），包括pip

2. 运行命令（Win + R，键入CMD），将当前目录更改为“ TopixPop / Win32”

3. 如果您的Python是AMD64版本，请在控制台中键入`pip install wordcloud-1.7.0-cp38-cp38-win_amd64.whl`。如果您的PythoSn是i386版本，请键入`pip install wordcloud- 1.7.0-cp38-cp38-win_amd64.whl`

4.安装需求。在控制台中输入“ pip install -r requirements.txt”

3.运行（双击）"mGenerate.pyw"

# 已知的Bug

1. 删除停用词列表元素的错误

# To-do

1. 制作一个Win32安装程序

2. ~~系统托盘图标~~（完成）

3. Wordcloud蒙版

4. 支持刷新、还原桌面背景