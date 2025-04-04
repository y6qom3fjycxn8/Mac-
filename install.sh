#!/bin/bash

echo "开始安装连接监控程序..."

# 检查是否安装了pip3
if ! command -v pip3 &> /dev/null; then
    echo "未找到pip3，请先安装Python3"
    exit 1
fi

# 安装依赖
echo "正在安装依赖..."
pip3 install -r requirements.txt || { echo "依赖安装失败"; exit 1; }

# 运行打包命令
echo "正在打包应用程序..."
python3 setup.py py2app || { echo "打包失败"; exit 1; }

# 检查是否成功生成应用程序
if [ ! -d "dist/连接监控.app" ]; then
    echo "应用程序生成失败"
    exit 1
fi

# 复制应用程序到应用程序文件夹
echo "正在安装应用程序..."
cp -r "dist/连接监控.app" "/Applications/" || { echo "复制到应用程序文件夹失败"; exit 1; }

echo "应用程序已安装到应用程序文件夹"
echo "请注意："
echo "1. 首次运行时需要授予屏幕录制和辅助功能权限"
echo "2. 请将三张图片(full.jpg、connected.jpg、disconnected.jpg)放入以下目录："
echo "   /Applications/连接监控.app/Contents/Resources/"
echo "安装完成！" 