#!/bin/bash

# 下载运行脚本
echo "下载运行脚本..."
curl -L -o "run.sh" https://raw.githubusercontent.com/qtaxm/Mac-/main/run.sh

# 下载模板图片
echo "下载模板图片..."
curl -L -o "disconnected.png" https://raw.githubusercontent.com/qtaxm/Mac-/main/disconnected.png
curl -L -o "connected.png" https://raw.githubusercontent.com/qtaxm/Mac-/main/connected.png
curl -L -o "full.png" https://raw.githubusercontent.com/qtaxm/Mac-/main/full.png

# 检查文件
if [ ! -f "run.sh" ]; then
    echo "错误：run.sh 下载失败"
    exit 1
fi

if [ ! -f "disconnected.png" ]; then
    echo "错误：disconnected.png 下载失败"
    exit 1
fi

if [ ! -f "connected.png" ]; then
    echo "错误：connected.png 下载失败"
    exit 1
fi

if [ ! -f "full.png" ]; then
    echo "错误：full.png 下载失败"
    exit 1
fi

# 添加执行权限
chmod +x "run.sh"

# 运行脚本
echo "启动监控程序..."
./run.sh 