#!/bin/bash

# 获取用户桌面路径
DESKTOP="$HOME/Desktop"

# 下载所需文件
echo "下载运行脚本..."
curl -L -o "$DESKTOP/run.sh" https://raw.githubusercontent.com/qtaxm/Mac-/main/run.sh

echo "下载模板图片..."
echo "下载 full.png..."
curl -L -o "$DESKTOP/full.png" https://raw.githubusercontent.com/qtaxm/Mac-/main/full.png
if [ ! -f "$DESKTOP/full.png" ]; then
    echo "错误：full.png 下载失败"
    exit 1
fi

echo "下载 connected.png..."
curl -L -o "$DESKTOP/connected.png" https://raw.githubusercontent.com/qtaxm/Mac-/main/connected.png
if [ ! -f "$DESKTOP/connected.png" ]; then
    echo "错误：connected.png 下载失败"
    exit 1
fi

echo "下载 disconnected.png..."
curl -L -o "$DESKTOP/disconnected.png" https://raw.githubusercontent.com/qtaxm/Mac-/main/disconnected.png
if [ ! -f "$DESKTOP/disconnected.png" ]; then
    echo "错误：disconnected.png 下载失败"
    exit 1
fi

# 添加执行权限
chmod +x "$DESKTOP/run.sh"

# 检查所有文件是否存在
for file in "run.sh" "full.png" "connected.png" "disconnected.png"; do
    if [ ! -f "$DESKTOP/$file" ]; then
        echo "错误：在桌面上找不到 $file"
        exit 1
    fi
done

# 运行脚本
echo "所有文件下载完成，启动监控程序..."
"$DESKTOP/run.sh"