# Mashiro Win32

Windows平台~~量身定做~~的Mashiro版本

# BETA

修复部分BUG，（即将）加入任务栏图标

# 部署

## Windows 10

1. 安装Python> = 3.7，包括pip

2. 运行Command（Win + R，键入CMD），进入目录" Mashiro / Win32"，然后在控制台中输入 `pip install -r requirements.txt`

3. 运行（双击）"mGenerate.pyw"

## Windows NT 6（Windows 7，Windows 8.1）

1. 安装Python == 3.8（必须为Python 3.8.X），包括pip

2. 运行命令（Win + R，键入CMD），将当前目录更改为“ Mashiro / Win32”

3. 如果您的Python是AMD64版本，请在控制台中键入`pip install wordcloud-1.7.0-cp38-cp38-win_amd64.whl`。如果您的Python是32位，请键入`pip install wordcloud- 1.7.0-cp38-cp38-win32.whl`

4.安装需求。在控制台中输入“ pip install -r requirements.txt”

3.运行（双击）"mGenerate.pyw"

# 已知的Bug

1. ~~无法修改爬虫(Spider)列表和屏蔽词(Stopwords)列表~~ （已解决）

2. ~~在Windows 7下没有对Emoji的支持~~ （已解决）

3. ~~配置文件中非ASCII字符编码问题~~ （已解决）

# To-do

1. ~~制作一个Win32安装程序~~(废除)

2. 系统托盘图标

3. Wordcloud蒙版
