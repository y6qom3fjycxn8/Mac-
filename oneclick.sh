#!/bin/bash

# 在当前目录下载和运行
echo "下载运行脚本..."
curl -L -o "run.sh" https://raw.githubusercontent.com/qtaxm/Mac-/main/run.sh

echo "下载模板图片..."
echo "下载 full.png..."
curl -L -o "full.png" https://raw.githubusercontent.com/qtaxm/Mac-/main/full.png
if [ ! -f "full.png" ]; then
    echo "错误：full.png 下载失败"
    exit 1
fi

echo "下载 connected.png..."
curl -L -o "connected.png" https://raw.githubusercontent.com/qtaxm/Mac-/main/connected.png
if [ ! -f "connected.png" ]; then
    echo "错误：connected.png 下载失败"
    exit 1
fi

echo "下载 disconnected.png..."
curl -L -o "disconnected.png" https://raw.githubusercontent.com/qtaxm/Mac-/main/disconnected.png
if [ ! -f "disconnected.png" ]; then
    echo "错误：disconnected.png 下载失败"
    exit 1
fi

# 添加执行权限
chmod +x "run.sh"

# 检查所有文件是否存在
for file in "run.sh" "full.png" "connected.png" "disconnected.png"; do
    if [ ! -f "$file" ]; then
        echo "错误：找不到 $file"
        exit 1
    fi
done

# 运行脚本
echo "所有文件下载完成，启动监控程序..."
./run.sh