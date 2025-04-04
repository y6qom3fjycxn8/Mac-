#!/bin/bash

# 获取用户桌面路径
DESKTOP="$HOME/Desktop"

# 下载所需文件
echo "下载运行脚本..."
curl -o "$DESKTOP/run.sh" https://raw.githubusercontent.com/qtaxm/Mac-/main/run.sh

echo "下载模板图片..."
curl -o "$DESKTOP/full.png" https://raw.githubusercontent.com/qtaxm/Mac-/main/full.png
curl -o "$DESKTOP/connected.png" https://raw.githubusercontent.com/qtaxm/Mac-/main/connected.png
curl -o "$DESKTOP/disconnected.png" https://raw.githubusercontent.com/qtaxm/Mac-/main/disconnected.png

# 添加执行权限
chmod +x "$DESKTOP/run.sh"

# 运行脚本
echo "启动监控程序..."
"$DESKTOP/run.sh"