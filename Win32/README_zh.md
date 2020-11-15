# TopixPop Win32

Windows平台~~量身定做~~的TopixPop版本

# BETA 2 20201115

优化：

1. 支持手动刷新；

2. 退出前自动恢复壁纸。

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

# Bug列表

1. 退出后无法还原图片位置；

# To-do

1. 制作一个Win32安装程序

2. ~~系统托盘图标~~（完成）

3. Wordcloud蒙版

4. ~~支持刷新、还原桌面背景~~（完成）